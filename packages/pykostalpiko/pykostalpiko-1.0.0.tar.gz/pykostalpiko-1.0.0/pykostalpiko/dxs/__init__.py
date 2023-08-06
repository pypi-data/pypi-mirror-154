"""DxsEntries general constants and methods."""
from pykostalpiko.dxs.current_values import LIST as current_values_LIST
from pykostalpiko.dxs.entry import Descriptor
from pykostalpiko.dxs.inverter import LIST as inverter_LIST
from pykostalpiko.dxs.statistics import LIST as statistics_LIST

LIST: list[Descriptor] = current_values_LIST + statistics_LIST + inverter_LIST


def find_descriptor_by_id(dxs_id: int) -> Descriptor:
    """Find a descriptor by its id."""
    for descriptor in LIST:
        if descriptor.key == dxs_id:
            return descriptor

    raise ValueError(f"No descriptor found for id {dxs_id}")
