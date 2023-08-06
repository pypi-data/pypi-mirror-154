"""CoreBluetooth application that calls into the PeripheralManagerDelegate"""

#    Copyright (c)  2021  Allthenticate

# Native Libraries
import asyncio
import logging
import struct
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Set

# Core Bluetooth related
from CoreBluetooth import (  # type: ignore
    CBUUID,
    CBAdvertisementDataLocalNameKey,
    CBAdvertisementDataServiceUUIDsKey,
    CBCentral,
    CBManagerStatePoweredOff,
    CBManagerStatePoweredOn,
    CBMutableCharacteristic,
)
from Foundation import NSData, NSString  # type: ignore

# Able related
from able.corebluetooth.advertisement import CBLEAdvertisement
from able.corebluetooth.characteristic import CBCharacteristic
from able.corebluetooth.peripheral_manager_delegate import (
    PeripheralManagerDelegate,  # type: ignore
)
from able.corebluetooth.service import ABleCBService
from able.plugins.ibeacon import ABleiBeacon
from able.utils import DeviceCallbackData

if TYPE_CHECKING:
    from able.advertisement import ABleAdvertisement
    from able.central import ABleCentral
    from able.characteristic import ABleCharacteristic
    from able.service import ABleService

logger = logging.getLogger(name=__name__)


class CBApplication:
    """
    The high level application that abstracts the pyobjc corebluetooth calls

    :param name: the name that this application has
    """

    def __init__(self, name: str, *args, **kwargs):  # pylint: disable=unused-argument
        """Initializer for the CoreBluetooth application"""
        self.name: str = name

        self.peripheral_manager_delegate: PeripheralManagerDelegate = (
            PeripheralManagerDelegate.alloc().init()
        )

        # Allow the peripheral manager delegate to reference the app
        self.peripheral_manager_delegate.assign_app(self)

        # Services related
        self.services: List[ABleCBService] = []

        # Adverts related
        self.advertisement_data: Dict[
            CBAdvertisementDataLocalNameKey, CBAdvertisementDataServiceUUIDsKey
        ] = {}

        # Communication related
        self.marked_characteristic: Optional["ABleCharacteristic"] = None

        # Connection/subscription related
        self.has_new_central = asyncio.Event()
        self.new_connection_queue: Set["ABleCentral"] = set()
        self.connected_centrals: Dict[str, "ABleCentral"] = {}
        self.user_connect_callback: Optional[Callable] = None
        self.user_disconnect_callback: Optional[Callable] = None

        # Other
        self.start_counter = 0

        self.peripheral_ready = asyncio.Event()

    async def setup(self) -> None:
        """Setup the peripheral manager delegate and give it a reference to this app"""
        await self.peripheral_manager_delegate.setup()

    def state_change_callback(self, peripheral_state: int) -> None:
        """
        This is called anytime the state changes and will then trigger a user-defined callback

        :param peripheral_state: The current CoreBluetooth state of the Bluetooth controller
        :return: None
        """
        if peripheral_state == CBManagerStatePoweredOff:
            # Bluetooth off
            pass
        elif peripheral_state == CBManagerStatePoweredOn:
            # Bluetooth on
            logger.debug(
                "Trying to restart our advertisements (should force even when coming out of sleep)"
            )
            self.start_counter = 0
            asyncio.create_task(self.restart_advertising())

    def connect_callback(
        self, central: CBCentral, callback_data: DeviceCallbackData
    ) -> None:
        """
        Handler for the new connections/subscriptions being signalled from Core Bluetooth.
        Core Bluetooth does not offer an API for connection callbacks, just characteristic
        subscription callbacks. For the sake of cross-platform BLE abstraction, we treat the
        subscriptions the same as connections. Adds an entry to the new connection queue so
        that a peripheral server can accept the new connection. Adds a new ABleCentral to
        the connected centrals dictionary. Calls an optional user defined callback last.

        :param callback_data: data including the identifier required to create ABleCentral
        :return: None
        """
        from able.central import ABleCentral  # pylint: disable=import-outside-toplevel

        if callback_data.identifier in self.connected_centrals:
            logger.warning(
                "Client already connected, likely they already subscribed, connect cb is a NOOP"
            )
            return

        logger.info(f"New connection from {callback_data}")

        # Create the new central
        new_central: "ABleCentral" = ABleCentral(
            application=self, identifier=callback_data.identifier, central_obj=central
        )
        self.new_connection_queue.add(new_central)
        self.connected_centrals[callback_data.identifier] = new_central
        new_central.char_subscriptions.append(callback_data.char_uuid)

        # Add a receive queue for each characteristic
        for service in self.services:
            for char in service.characteristics.values():
                new_central.char_queues[hash(char)] = asyncio.Queue()
                logger.debug(
                    f"Queue was created for characteristic {char.uuid} on central {new_central}"
                )

        # Set the new connection event if it is not already set
        if not self.has_new_central.is_set():
            self.has_new_central.set()

        logger.debug(f"{self.new_connection_queue} | {self.connected_centrals}")

        if self.user_connect_callback:
            try:
                self.user_connect_callback(callback_data)
            except TypeError:
                logger.exception(
                    "User-defined connection callback is not able to be called with the argument given"
                )

    def disconnect_callback(self, callback_data: DeviceCallbackData) -> None:
        """
        Handler for disconnections being signalled by Core Bluetooth. Updates the disconnected ABleCentral's state to be
        disconnected. Removes the central from the connected centrals dictionary (if it was there, it will not be
        present if the connection was established before the application was running) and the new connection queue
        if it is present. Calls an optional user defined callback last.

        :param callback_data: data regarding the central which disconnected
        :return: None
        """

        from able.central import ABleCentral  # pylint: disable=import-outside-toplevel

        logger.info(f"Disconnect from {callback_data}")

        # Get the central which disconnected the centrals state to disconnected
        disconnecting_central: ABleCentral = self.connected_centrals[
            callback_data.identifier
        ]
        disconnecting_central.disconnected_event.set()

        # Remove from the connected centrals dict and the NCQ
        self.new_connection_queue.discard(disconnecting_central)
        self.connected_centrals.pop(callback_data.identifier)

        # If we no longer have any connections, unset the event
        if len(self.new_connection_queue) == 0:
            self.has_new_central.clear()

        logger.info(f"{self.new_connection_queue} | {self.connected_centrals}")

        if self.user_disconnect_callback:
            try:
                self.user_disconnect_callback(callback_data)
            except TypeError:
                logger.exception(
                    "User-defined disconnect callback is not able to be called with the argument given"
                )

    async def add_advertisement(
        self, advertisement: "ABleAdvertisement", refresh: bool = False
    ) -> None:
        """Adds an le_advertisement object to the application"""

        # Fetch the core bluetooth advert from the wrapper
        le_advertisement = advertisement.le_advertisement

        # Input validation
        if not isinstance(le_advertisement, CBLEAdvertisement):
            raise TypeError(
                f"Advertisement error is the wrong type for this platform (CoreBluetooth): {type(le_advertisement)}"
            )

        if self.advertisement_data and not refresh:
            raise ValueError(
                "There is already an advertisement in the application (CoreBluetooth supports only 1)"
            )

        # Add the advertisement to the application
        uuids: List[CBUUID] = [
            CBUUID.alloc().initWithString_(service_uuid)
            for service_uuid in le_advertisement.service_uuids
        ]
        self.advertisement_data = {
            CBAdvertisementDataLocalNameKey: le_advertisement.local_name,
            CBAdvertisementDataServiceUUIDsKey: uuids,
        }

        le_advertisement.application = self

    async def advertise_ibeacon(self, advertisement: ABleiBeacon) -> None:
        """
        Adds an iBeacon and then advertises it

        TODO: How many of these can a peripheral support?
        TODO (Chad): Figure out a more general way to do this in the future

        Ref: https://github.com/watr/mbeacon
        Ref: https://titanwolf.org/Network/Articles/Article?AID=b0003beb-d37f-4d08-a62f-16e1e93cc19b
        Ref: https://blendedcocoa.com/blog/2013/11/02/mavericks-as-an-ibeacon/
        """
        # I don't think we need this, 0 sounds fine
        measured_power = 0

        # We must convert everything into a RAW data buffer (this functionality is not supported/documented by Apple)
        raw_data = (
            advertisement.uuid.bytes
            + b"".join(advertisement.major)
            + b"".join(advertisement.minor)
            + struct.pack("B", measured_power)
        )

        # Convert our data to NSString and NSData so that the API is happy
        beacon_nsstring = NSString.alloc().initWithString_("kCBAdvDataAppleBeaconKey")
        data = NSData.alloc().initWithBytes_length_(raw_data, len(raw_data))
        beacon_name = NSString.alloc().initWithString_("aBeacon")

        # Construct our dictionary and advertise it!
        adv_data = {
            CBAdvertisementDataLocalNameKey: beacon_name,
            beacon_nsstring: data,
        }
        await self.peripheral_manager_delegate.startAdvertising_(adv_data)
        logger.info("Ibeacon added!")

    async def refresh_advertisement(self, advertisement: "ABleAdvertisement") -> None:
        """Refreshes the le_advertisement object and calls startAdvertising again with the new
        advertisement data"""
        self.peripheral_manager_delegate.stopAdvertising()
        await self.add_advertisement(advertisement, refresh=True)
        await self.restart_advertising()

    async def restart_advertising(self) -> bool:
        """Simply re-advertise our existing advertisement data.  This is useful when coming out sleep mode."""
        if self.advertisement_data is None:
            return False

        self.start_counter += 1
        try:
            await self.peripheral_manager_delegate.startAdvertising_(
                self.advertisement_data
            )
            self.start_counter = 0
            return True
        except asyncio.TimeoutError as e:
            logger.debug("Failed to start advertising, retrying...")
            if self.start_counter < 10:
                await self.start_interface()
            else:
                raise RecursionError(
                    "Failed to start advertising for 10 consecutive times, ending execution..."
                ) from e
            return False

    async def start_interface(self) -> None:
        """
        Starts up the CoreBluetooth interface

        :return: None
        """
        logger.debug(f"Advertisement Data: {self.advertisement_data}")

        for service in self.services:
            logger.debug(f"Adding service: {service.uuid}")
            await self.peripheral_manager_delegate.addService(service.obj)

        self.start_counter += 1
        try:
            await self.peripheral_manager_delegate.startAdvertising_(
                self.advertisement_data
            )
            self.start_counter = 0
        except asyncio.TimeoutError as e:
            logger.debug("Failed to start advertising, retrying...")
            if self.start_counter < 10:
                await self.start_interface()
            else:
                raise RecursionError(
                    "Failed to start advertising for 10 consecutive times, ending execution..."
                ) from e

    def add_service(self, service: "ABleCBService") -> None:
        """
        Adds a CoreBluetooth service to the application, this must be done before running start_application()

        :raises TypeError: if service is not of type ABleCBService
        :raises RuntimeError: if the service has already been added to the application

        :param service: the service to add to the CB application
        :return: None
        """
        if not isinstance(service, ABleCBService):
            raise TypeError(
                f"The service that is trying to be added is the wrong type for this platform (CoreBluetooth):"
                f" {type(service)}"
            )

        if service in self.services:
            raise RuntimeError(f"Already added {service} to the application.")

        self.services.append(service)

    def add_characteristic(
        self,
        service: "ABleService",
        characteristic: CBCharacteristic,
        is_comms_char: bool = False,
    ) -> None:
        """Adds a characteristic to the application

        :param is_comms_char: if `True` the characteristic will become the comms characteristic, defaults to `False`
        :param service: the service which the characteristic will be added under
        :param characteristic: the characteristic you wish to add to the service
        :return: None
        """

        if not isinstance(service, ABleCBService):
            raise TypeError(
                "The service must be the of type ABleCBService to add to a Bluez application"
            )
        if not isinstance(characteristic, CBCharacteristic):
            raise TypeError(
                "The characteristic must be of the type BluezCharacteristic to add to a Bluez application"
            )

        # Make sure there wasn't already a characteristic with that UUID
        if characteristic.uuid in service.characteristics.keys():
            raise ValueError(
                "Adding a characteristic with a UUID that matches another characteristic in the service!"
            )

        # Add the characteristic to the service
        service.characteristics[characteristic.uuid] = characteristic

        # Link the characteristic to the service
        characteristic.service = service
        characteristic.application = self

        if is_comms_char:
            # Now handle marking updating by removing the old one and adding the new one
            if self.marked_characteristic is not None:
                logger.debug(
                    f"{self.marked_characteristic} is no longer marked for comms."
                )
                self.marked_characteristic.is_marked = False  # type: ignore

            characteristic.is_marked = True  # type: ignore
            self.marked_characteristic = characteristic
            logger.debug(f"{self.marked_characteristic} is now marked for comms")

        # Add the characteristic to the Core Bluetooth service
        chars: List[CBMutableCharacteristic] = [
            char.obj for char in service.characteristics.values()  # type: ignore
        ]
        service.obj.setCharacteristics_(chars)

    def stop(self) -> None:
        """Stop the peripheral server"""
        self.peripheral_manager_delegate.peripheral_manager.removeAllServices()
        self.peripheral_manager_delegate.stopAdvertising()

    def add_connect_callback(self, callback: Callable) -> None:
        """
        Adds a user-defined callback function to the application to be called after connecting to a central device.
        :param callback: the function to be called after a successful connection
        """
        self.user_connect_callback = callback

    def add_disconnect_callback(self, callback: Callable) -> None:
        """
        Adds a user-defined callback function to the application to be called after disconnecting from a central device.
        :param callback: the function to be called after a successful disconnect
        """
        self.user_disconnect_callback = callback

    async def disconnect(
        self, central: "ABleCentral"
    ):  # pylint: disable=unused-argument, no-self-use
        """Disconnect from central"""
        logger.warning("Serverside disconnect is not currently supported on macOS")

    @property
    def communication_characteristic(self) -> "ABleCharacteristic":
        """Property which returns the marked comms characteristic or raises an exception"""
        if self.marked_characteristic is None:
            raise RuntimeError(
                "Attempted to fetch comms characteristic without defining one"
            )
        return self.marked_characteristic
