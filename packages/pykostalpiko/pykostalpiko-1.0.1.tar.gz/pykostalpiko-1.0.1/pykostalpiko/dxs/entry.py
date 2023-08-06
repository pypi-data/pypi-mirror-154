"""Description of DxsEntries."""
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class DescriptorOptions:
    """Options for the Descriptor class."""

    def __init__(
        self,
        configurable: bool = False,
        mapper_function: Callable[[Any], Any] = None,
        multiplication_factor: float = 1,
    ) -> None:
        """Constructor."""
        self.configurable = configurable
        self.mapper_function = mapper_function
        self.multiplication_factor = multiplication_factor


@dataclass
class Descriptor:
    """Data structure to describe a DxsEntry"""

    def __init__(
        self,
        key: int,
        name: str,
        unit: str = None,
        options: DescriptorOptions = DescriptorOptions(),
    ) -> None:
        """Constructor."""
        self.key = key
        self.name = name
        self.unit = unit
        self.options = options


@dataclass
class ConfigurableDescriptor(Descriptor):
    """Descriptor data structure, but configurable turned on."""

    def __init__(
        self,
        key: int,
        name: str,
        unit: str = None,
        options: DescriptorOptions = DescriptorOptions(configurable=True),
    ) -> None:
        super().__init__(key, name, unit, options)


class MapperException(Exception):
    """Exception raised when a mapping is not found."""
