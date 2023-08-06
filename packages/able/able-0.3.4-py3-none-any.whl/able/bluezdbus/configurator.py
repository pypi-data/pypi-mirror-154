"""
This is a helper file used for configuring the bluez conf file
"""

import logging
import os
import sys
import xml.etree.ElementTree as ET
from typing import Optional

# Setup logging
logger = logging.getLogger(name=__name__)


def configure_bluez_conf_file(
    peripheral_name: str = "ABle", user_name: str = "root", path: Optional[str] = None
) -> bool:
    """
    This function (must have root permissions to modify the needed file) will modify the conf file dbus
    uses for Bluez such that a user can run an application with a given name

    :param peripheral_name: The name of your application (defaults to ABle)
    :param user_name: The user that will be granted permission (defaults to root)
    :return: True if the configuration file was changed, otherwise False
    """
    # Make sure they are running as root
    if os.geteuid() != 0:
        logger.error("This configuration can only be ran as root!")
        sys.exit(1)

    # Parse the current config file
    if path is None:
        path = "/etc/dbus-1/system.d/bluetooth.conf"
        logger.info(f"No path given for updating permissions, defaulting to {path}")

    tree = ET.parse(path)
    config = tree.getroot()

    root_policy = None
    user_policy = None

    did_change = False

    # First find the user="root" policy
    for policy in config:

        # Check for the root policy
        if policy.attrib == {"user": "root"}:
            root_policy = policy
            continue

        # Check for user policy
        if policy.attrib == {"user": user_name}:
            user_policy = policy
            continue

    # Let's validate that the root policy has a rule to send to this application, root needs to be able to send
    if not root_policy.findall(
        f"allow[@send_destination='org.bluez.{peripheral_name}']"
    ):
        logger.debug(f"Send destination for {peripheral_name} not found, inserting...")
        child = ET.Element(
            "allow", {"send_destination": f"org.bluez.{peripheral_name}"}
        )
        root_policy.append(child)
        did_change = True
    else:
        logger.debug("Root policy already configured...")

    # Make sure a user policy exists
    if user_policy is None:
        logger.debug(f"No user policy exists, creating one for {user_name}")
        user_policy = ET.Element("policy", {"user": user_name})
        config.append(user_policy)
        did_change = True
    else:
        logger.debug(f"A user policy already exists for {user_name}")

    # Make sure all the rules in the user policy exist, the user needs to be own the service org.bluez.<peripheral name>
    if not user_policy.findall(f"allow[@own='org.bluez.{peripheral_name}']"):
        logger.debug(
            f"Own rule for {user_name} for application {peripheral_name} not found, inserting..."
        )
        child = ET.Element("allow", {"own": f"org.bluez.{peripheral_name}"})
        user_policy.append(child)
        did_change = True
    else:
        logger.debug("User policy is already configured.")

    tree.write(path)

    return did_change
