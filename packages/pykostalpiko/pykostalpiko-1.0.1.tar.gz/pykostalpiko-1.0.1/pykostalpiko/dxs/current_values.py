"""DxsEntries for all current values."""
from dataclasses import dataclass

from pykostalpiko.dxs.entry import Descriptor, DescriptorOptions, MapperException


@dataclass
class PVGenerator:
    """DxsEntries concerning the generation of energy by the photovoltaic generator."""

    @dataclass
    class CombinedInput:
        """DxsEntries describing the combined input."""

        POWER = Descriptor(33556736, "PV Combined Input", "W")

        LIST = [POWER]

    @dataclass
    class DcInput1:
        """DxsEntries describing the DC input 1."""

        CURRENT = Descriptor(33555201, "DC Input 1 Current", "A")
        VOLTAGE = Descriptor(33555202, "DC Input 1 Voltage", "V")
        POWER = Descriptor(33555203, "DC Input 1 Power", "W")

        LIST = [CURRENT, VOLTAGE, POWER]

    @dataclass
    class DcInput2:
        """DxsEntries describing the DC Input 2."""

        CURRENT = Descriptor(33555457, "DC Input 2 Current", "A")
        VOLTAGE = Descriptor(33555458, "DC Input 2 Voltage", "V")
        POWER = Descriptor(33555459, "DC Input 2 Power", "W")

        LIST = [CURRENT, VOLTAGE, POWER]

    LIST = CombinedInput.LIST + DcInput1.LIST + DcInput2.LIST


@dataclass
class House:
    """DxsEntries concerning the power consumption of the house."""

    SELF_CONSUMPTION = Descriptor(83888128, "Self Consumption", "W")

    @dataclass
    class CoveredBy:
        """DxsEntries describing where the power of the house comes from."""

        SOLAR_GENERATOR = Descriptor(83886336, "Solar Generator", "W")
        BATTERY = Descriptor(83886592, "Battery", "W")
        GRID = Descriptor(83886848, "Grid", "W")

        LIST = [SOLAR_GENERATOR, BATTERY, GRID]

    @dataclass
    class PhaseConsumption:
        """DxsEntries describing on which phases the power consumption of the house is."""

        PHASE_1 = Descriptor(83887106, "Phase 1", "W")
        PHASE_2 = Descriptor(83887362, "Phase 2", "W")
        PHASE_3 = Descriptor(83887618, "Phase 3", "W")

        LIST = [PHASE_1, PHASE_2, PHASE_3]

    LIST = [SELF_CONSUMPTION] + CoveredBy.LIST + PhaseConsumption.LIST


@dataclass
class Battery:
    """DxsEntries concerning the battery."""

    CURRENT_DIRECTION_CHARING = "Charging"
    CURRENT_DIRECTION_DISCHARGING = "Discharging"

    def _batter_current_direction_mapper(self, val: int) -> str:
        """Map the battery current direction to a string."""

        if val == 0:
            return self.CURRENT_DIRECTION_DISCHARGING
        if val == 1:
            return self.CURRENT_DIRECTION_CHARING
        raise MapperException("Failed mapping Battery Current Direction", val)

    VOLTAGE = Descriptor(33556226, "Battery Voltage", "V")
    CHARGE = Descriptor(33556229, "Battery Charge", "%")
    CURRENT = Descriptor(33556238, "Battery Current", "A")
    CURRENT_DIRECTION = Descriptor(
        33556230,
        "Battery Current Direction",
        DescriptorOptions(mapper_function=_batter_current_direction_mapper),
    )
    CYCLES = Descriptor(33556228, "Battery Cycles")
    TEMPERATURE = Descriptor(33556227, "Battery Temperature", "°C")

    LIST = [VOLTAGE, CHARGE, CURRENT, CURRENT_DIRECTION, CYCLES, TEMPERATURE]


@dataclass
class Grid:
    """DxsEntries concerning the power grid."""

    @dataclass
    class Parameters:
        """DxsEntries describing the current parameters of the grid."""

        OUTPUT_POWER = Descriptor(67109120, "Output Power", "W")
        FREQUENCY = Descriptor(67110400, "Frequency", "Hz")
        POWER_FACTOR = Descriptor(67110656, "Power Factor")
        LIMITATION = Descriptor(67110144, "Limitation", "%")

        LIST = [OUTPUT_POWER, FREQUENCY, POWER_FACTOR, LIMITATION]

    @dataclass
    class Phase1:
        """DxsEntries describing the current parameters of the phase 1 from the power grid."""

        CURRENT = Descriptor(67109377, "Phase 1 Current", "A")
        VOLTAGE = Descriptor(67109378, "Phase 1 Voltage", "V")
        POWER = Descriptor(67109379, "Phase 1 Power", "W")

        LIST = [CURRENT, VOLTAGE, POWER]

    @dataclass
    class Phase2:
        """DxsEntries describing the current parameters of the phase 2 from the power grid."""

        CURRENT = Descriptor(67109633, "Phase 2 Current", "A")
        VOLTAGE = Descriptor(67109634, "Phase 2 Voltage", "V")
        POWER = Descriptor(67109635, "Phase 2 Power", "W")

        LIST = [CURRENT, VOLTAGE, POWER]

    @dataclass
    class Phase3:
        """DxsEntries describing the current parameters of the phase 3 from the power grid."""

        CURRENT = Descriptor(67109889, "Phase 3 Current", "A")
        VOLTAGE = Descriptor(67109890, "Phase 3 Voltage", "V")
        POWER = Descriptor(67109891, "Phase 3 Power", "W")

        LIST = [CURRENT, VOLTAGE, POWER]

    LIST = Parameters.LIST + Phase1.LIST + Phase2.LIST + Phase3.LIST


@dataclass
class AnalogInputs:
    """DxsEntries concerning the analog inputs."""

    INPUT_1 = Descriptor(167772417, "Analoginput 1", "V")
    INPUT_2 = Descriptor(167772673, "Analoginput 2", "V")
    INPUT_3 = Descriptor(167772929, "Analoginput 3", "V")
    INPUT_4 = Descriptor(167773185, "Analoginput 4", "V")

    LIST = [INPUT_1, INPUT_2, INPUT_3, INPUT_4]


@dataclass
class S0Input:
    """DxsEntries concerning the S0 input."""

    PULSE_COUNT = Descriptor(184549632, "Pulse Count")
    PULSE_COUNT_TIMEFRAME = Descriptor(150995968, "Pulse Count Timeframe", "s")

    LIST = [PULSE_COUNT, PULSE_COUNT_TIMEFRAME]


LIST = (
    PVGenerator.LIST
    + House.LIST
    + Battery.LIST
    + Grid.LIST
    + AnalogInputs.LIST
    + S0Input.LIST
)
