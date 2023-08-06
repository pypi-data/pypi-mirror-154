"""DxsEntries for all statistics."""
from dataclasses import dataclass

from pykostalpiko.dxs.entry import Descriptor, DescriptorOptions


@dataclass
class Day:
    """DxsEntries for the daily statistics."""

    YIELD = Descriptor(251658754, "Yield", "Wh")
    HOME_CONSUMPTION = Descriptor(251659010, "Home Consumption", "Wh")
    SELF_CONSUMPTION = Descriptor(251659266, "Self Consumption", "Wh")
    SELF_CONSUMPTION_RATE = Descriptor(251659278, "Self Consumtion Rate", "%")
    DEGREE_OF_SELF_SUFFICIENCY = Descriptor(
        251659279, "Degree of Self Sufficiency", "%"
    )

    LIST = [
        YIELD,
        HOME_CONSUMPTION,
        SELF_CONSUMPTION,
        SELF_CONSUMPTION_RATE,
        DEGREE_OF_SELF_SUFFICIENCY,
    ]


@dataclass
class Total:
    """DxsEntries for the total statistics."""

    YIELD = Descriptor(
        251658753, "Yield", "Wh", DescriptorOptions(multiplication_factor=1000)
    )
    HOME_CONSUMPTION = Descriptor(
        251659009,
        "Home Consumption",
        "Wh",
        DescriptorOptions(multiplication_factor=1000),
    )
    SELF_CONSUMPTION = Descriptor(
        251659265,
        "Self Consumption",
        "Wh",
        DescriptorOptions(multiplication_factor=1000),
    )
    SELF_CONSUMPTION_RATE = Descriptor(251659280, "Self Consumtion Rate", "%")
    DEGREE_OF_SELF_SUFFICIENCY = Descriptor(
        251659281, "Degree of Self Sufficiency", "%"
    )
    OPERATION_TIME = Descriptor(251658496, "Operation Time", "h")

    LIST = [
        YIELD,
        HOME_CONSUMPTION,
        SELF_CONSUMPTION,
        SELF_CONSUMPTION_RATE,
        DEGREE_OF_SELF_SUFFICIENCY,
        OPERATION_TIME,
    ]


LIST = Day.LIST + Total.LIST
