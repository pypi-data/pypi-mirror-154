"""DxsEntries concering the properties of the inverter itself."""
from dataclasses import dataclass

from pykostalpiko.dxs.entry import (
    ConfigurableDescriptor,
    Descriptor,
    DescriptorOptions,
    MapperException,
)


def _operation_status_mapper(val: int) -> str:
    """Map the operation status to a string."""

    if val == 0:
        return "Off"
    if val == 1:
        return "Idle"
    if val == 2:
        return "Starting"
    if val == 3:
        return "Feed MPP"
    if val == 4:
        return "Deactivated"
    if val == 5:
        return "Feed"
    raise MapperException("Failed mapping Operation Status", val)


OPERATION_STATUS = Descriptor(
    16780032,
    "Operation Status",
    DescriptorOptions(mapper_function=_operation_status_mapper),
)
SERIAL_NUMBER = Descriptor(16777728, "Serial Number")
ARTICLE_NUMBER = Descriptor(16777472, "Article Number")
COUNTRY_SETTINGS = Descriptor(16779522, "Country Settings")
COUNTRY_SETTINGS_VERSION = Descriptor(16779521, "Country Settings Version")

NAME = ConfigurableDescriptor(16777984, "Name")

# TODO: /settings/general/login


@dataclass
class Versions:
    """DxsEntries describing the versions of the inverter."""

    USER_INTERFACE = Descriptor(16779267, "User Interface")
    FIRMWARE = Descriptor(16779265, "Firmware")
    HARDWARE = Descriptor(16779266, "Hardware")
    # This is likely some abbreviation
    PAR = Descriptor(16779268, "PAR")

    LIST = [USER_INTERFACE, FIRMWARE, HARDWARE, PAR]


@dataclass
class Communication:
    """DxsEntries describing the communication with the inverter."""

    INVERTER_ADDRESS = ConfigurableDescriptor(117441025, "Inverter Address")

    @dataclass
    class Network:
        """DxsEntries describing the network connection with the inverter."""

        MAC_ADDRESS = Descriptor(117440811, "MAC Address")

        @dataclass
        class IPAddress:
            """DxsEntries describing the IPv4 Address."""

            PART_1 = ConfigurableDescriptor(117440791, "IP Address Part 1")
            PART_2 = ConfigurableDescriptor(117440792, "IP Address Part 2")
            PART_3 = ConfigurableDescriptor(117440793, "IP Address Part 3")
            PART_4 = ConfigurableDescriptor(117440794, "IP Address Part 4")

            LIST = [PART_1, PART_2, PART_3, PART_4]

        @dataclass
        class SubnetMask:
            """DxsEntries describing the Subnet Mask."""

            PART_1 = ConfigurableDescriptor(117440795, "Subnet Mask Part 1")
            PART_2 = ConfigurableDescriptor(117440796, "Subnet Mask Part 2")
            PART_3 = ConfigurableDescriptor(117440797, "Subnet Mask Part 3")
            PART_4 = ConfigurableDescriptor(117440798, "Subnet Mask Part 4")

            LIST = [PART_1, PART_2, PART_3, PART_4]

        @dataclass
        class DefaultGateway:
            """DxsEntries describing the Default Gateway."""

            PART_1 = ConfigurableDescriptor(117440799, "Default Gateway Part 1")
            PART_2 = ConfigurableDescriptor(117440800, "Default Gateway Part 2")
            PART_3 = ConfigurableDescriptor(117440801, "Default Gateway Part 3")
            PART_4 = ConfigurableDescriptor(117440802, "Default Gateway Part 4")

            LIST = [PART_1, PART_2, PART_3, PART_4]

        @dataclass
        class DNSServer:
            """DxsEntries describing the DNS Server."""

            PART_1 = ConfigurableDescriptor(117440807, "DNS Server Part 1")
            PART_2 = ConfigurableDescriptor(117440808, "DNS Server Part 2")
            PART_3 = ConfigurableDescriptor(117440809, "DNS Server Part 3")
            PART_4 = ConfigurableDescriptor(117440810, "DNS Server Part 4")

            LIST = [PART_1, PART_2, PART_3, PART_4]

        LIST = (
            [MAC_ADDRESS]
            + IPAddress.LIST
            + SubnetMask.LIST
            + DefaultGateway.LIST
            + DNSServer.LIST
        )

    LIST = [INVERTER_ADDRESS] + Network.LIST


@dataclass
class RS485:
    """DxsEntries describing the RS485 communication."""

    @classmethod
    def _protocol_mapper(cls, val: int) -> str:
        """Map the protocol to a string."""

        if val == 0:
            return "KOSTAL"
        if val == 1:
            return "Modbus"
        raise MapperException("Failed mapping Protocol", val)

    BUS_TERMINATION = ConfigurableDescriptor(117441027, "Bus Termination")
    BUS_BIAS_VOLTAGE = ConfigurableDescriptor(117441026, "Bus Bias Voltage")
    PROTOCOL = ConfigurableDescriptor(
        117441028, "Protocol", DescriptorOptions(mapper_function=_protocol_mapper)
    )
    BAUD_RATE = ConfigurableDescriptor(117441029, "Baud Rate")

    LIST = [BUS_TERMINATION, BUS_BIAS_VOLTAGE, PROTOCOL, BAUD_RATE]


# TODO: /settings/communication/modem


@dataclass
class PortalConfiguration:
    """DxsEntries describing the portal configuration."""

    ACTIVE_PORTAL = Descriptor(117441538, "Active Portal")
    # 117441542 is an unknown dxsId

    LIST = [ACTIVE_PORTAL]


@dataclass
class DataLogger:
    """DxsEntries describing the data logger."""

    LOG_INTERVAL = ConfigurableDescriptor(150995968, "Log Interval")

    LIST = [LOG_INTERVAL]


# TODO: /settings/generator-configuration

# TODO: /settings/battery-configuration

# TODO: /settings/switching-output

# TODO: /settings/analog-inputs

LIST = (
    [
        OPERATION_STATUS,
        SERIAL_NUMBER,
        ARTICLE_NUMBER,
        COUNTRY_SETTINGS,
        COUNTRY_SETTINGS_VERSION,
    ]
    + Versions.LIST
    + Communication.LIST
    + RS485.LIST
    + PortalConfiguration.LIST
    + DataLogger.LIST
)
