"""Wrapper around CoreBluetooth characteristic"""
# Native dependencies
import logging
import time
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union
from uuid import UUID

# Core Bluetooth dependencies
from CoreBluetooth import CBUUID, CBMutableCharacteristic  # type: ignore

# Able dependencies
from able.characteristic import ABleCharacteristic


class CBCharacteristicFlags(Enum):
    """CoreBluetooth characteristic properties"""

    BROADCAST = 0x0001
    READ = 0x0002
    WRITE_WITHOUT_RESPONSE = 0x0004
    WRITE = 0x0008
    NOTIFY = 0x0010
    INDICATE = 0x0020
    AUTHENTICATED_SIGNED_WRITES = 0x0040
    EXTENDED_PROPERTIES = 0x0080
    RELIABLE_WRITE = 0x0100
    WRITABLE_AUXILIARIES = 0x0200


class GATTAttributePermissions(Enum):
    """CoreBluetooth characteristic permissions"""

    READ = 0x1
    WRITE = 0x2
    READ_ENCRYPTION_REQUIRED = 0x4
    WRITE_ENCRYPTION_REQUIRED = 0x8


if TYPE_CHECKING:
    from able.central import ABleCentral
    from able.corebluetooth.application import CBApplication

logger = logging.getLogger(name=__name__)


class CBCharacteristic(ABleCharacteristic):
    """
    CoreBluetooth implementation of the BlessGATTCharacteristic

    :param characteristic_uuid: the uuid of the characteristic
    :type characteristic_uuid: Union[str, UUID]
    :param value: the initial value of the characteristic
    :param flags: the characteristic properties (read, write, notify, etc.)
    :param permissions: the characteristic permissions (read, write, read_encryption_required, etc.)
    :param notify_on_write: if True, all subscribed centrals will be notified when a write occurs
    """

    def __init__(
        self,
        characteristic_uuid: Union[str, UUID],
        value=None,
        flags=None,
        permissions=None,
        nickname: str = None,
        notify_on_write: bool = False,
    ):
        super().__init__(characteristic_uuid, value, flags, nickname, notify_on_write)

        # Additional Members
        self.application: Optional["CBApplication"] = None
        self.permissions = permissions

        # Keep track of whether or not this characteristic is the char for socket comms
        self.is_marked = False

        logger.debug(f"Setting up characteristic with flags: {self.flags}")

        # Convert flags to properties and permissions
        self.process_flags()

        # Initialize the Core Bluetooth object
        cb_uuid: CBUUID = CBUUID.alloc().initWithString_(self.uuid)
        cb_characteristic: CBMutableCharacteristic = (
            CBMutableCharacteristic.alloc().initWithType_properties_value_permissions_(
                cb_uuid, self.properties_value, self.value, self.permissions_value
            )
        )
        self.obj = cb_characteristic
        self.last_write = time.time()

    def __str__(self):
        return (
            f"CBCharacteristic [{self.uuid}]"
            if self.nickname is None
            else self.nickname
        )

    def __repr__(self):
        return str(self)

    def process_flags(self) -> None:
        """Convert characteristic flags to Core Bluetooth properties and permissions"""
        self.properties_value = sum(self.flags)

        # Permissions are inferred from properties UNLESS user sepcifies them
        if not self.permissions:
            self.permissions = []
            property_names = [x.name for x in self._flags]
            if "READ" in property_names:
                self.permissions.append(GATTAttributePermissions.READ.value)
            if "WRITE" in property_names:
                self.permissions.append(GATTAttributePermissions.WRITE.value)

        self.permissions_value = sum(self.permissions)

    async def broadcast(self, data: Union[bytes, str]):
        """Notify every subscribed central of a change to this characteristic

        :param data: the data to notify the centrals on
        """
        if self.application.connected_centrals:  # type: ignore
            await self.notify_central_of_change(None, data, notify_all=True)
        else:
            self.value = data  # type: ignore
            self.obj.setValue_(data)

    async def notify_central_of_change(  # pylint: disable=arguments-differ
        self,
        central: Optional["ABleCentral"],
        data: Union[bytes, str],
        notify_all=False,
    ) -> None:
        """
        Makes a Core Bluetooth call to notify only one central of a change to this characteristic

        :param notify_all: Notify every connected device?
        :param central: the central object that is notified
        :param data: the data to 'send' to the central by setting the value of this characteristic to and
            notifying only that central
        :return: None
        """
        # now = time.time()
        # if now - self.last_write < .001:
        #     await asyncio.sleep(.001)
        # self.last_write = now

        if not self.notifying:
            raise RuntimeWarning(
                "No central has indicated they want notifications on this characteristic, a central "
                "must subscribe before notifying/indicating"
            )

        if (
            self.application is None
            or self.application.peripheral_manager_delegate is None
        ):
            raise RuntimeError(
                "Unable to notify central of change without a bound application"
            )

        peripheral_manager = (
            self.application.peripheral_manager_delegate.peripheral_manager
        )

        try:
            # TODO(Chad): Make sure this cannot get stuck in an infinite loop
            while not peripheral_manager.updateValue_forCharacteristic_onSubscribedCentrals_(
                data, self.obj, None if notify_all else [central.obj]  # type: ignore
            ):
                logger.debug(
                    "Could not send data... peripheral delegate manager cache full... trying again in a bit"
                )
                self.application.peripheral_manager_delegate.peripheral_ready.clear()
                self.application.peripheral_manager_delegate.peripheral_ready.wait(
                    timeout=0.0001
                )
        except Exception:
            logger.exception(
                f"Exception caught when trying to notify {central}, are you sure the central is setup"
                "to notify on the characteristic?"
            )

        logger.debug("successfully sent data to central(s)")
        self.value = data  # type: ignore
        self.obj.setValue_(data)

    def set_value(self, value: bytearray, central_identifier: str) -> None:
        """Handles the request over CoreBluetooth to write a value to a characteristic

        :param value: value received from CoreBluetooth write callback
        :param central_identifier: uuid of the central device that wrote
        """

        if self.application is None:
            raise RuntimeError(
                "No application bound for characteristic, unable to perform actions"
            )

        if central_identifier not in self.application.connected_centrals:
            logger.warning(
                f"Received a write from {central_identifier} who we aren't tracking, ignoring"
            )
            return

        # Add the data to the recv queue
        logger.debug(f"Putting data {value} on queue")
        writer: "ABleCentral" = self.application.connected_centrals[central_identifier]

        writer.char_queues[hash(self)].put_nowait(bytes(value))

        logger.debug("Updating value of characteristic")
        self.value = bytes(value)
        self.obj.setValue_(value)

        if self.notify_on_write:
            self.broadcast(value)
