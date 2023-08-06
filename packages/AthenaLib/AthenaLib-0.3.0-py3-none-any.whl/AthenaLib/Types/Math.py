# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaLib.Types.ValueType import ValueType

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = [
    "Percent", "Degree"
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Degree(ValueType):
    _value:int|float
    def __init__(self, value: int|float):
        self.value = value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        if not isinstance(value, int|float):
            raise TypeError
        self._value = min(max(value, 0), 360)

    def __eq__(self, other:Degree| int | float) -> bool:
        if isinstance(other, Degree):
            return self.value == other.value
        elif isinstance(other,(int,float)):
            return self.value == other
        else:
            return NotImplemented

    def __str__(self):
        return f"{self.value}deg"
    def __repr__(self) -> str:
        return f"Degree(value={self.value})"
    def __hash__(self):
        return hash(self.value)

# ----------------------------------------------------------------------------------------------------------------------
class Percent(ValueType):
    _value:int|float
    def __init__(self, value: int|float):
        self.value = value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        if not isinstance(value, int|float):
            raise TypeError
        self._value = value

    def __eq__(self, other:Percent| int | float) -> bool:
        if isinstance(other, Percent):
            return self.value == other.value
        elif isinstance(other,(int,float)):
            return self.value == other
        else:
            return NotImplemented

    def __str__(self):
        return f"{self.value}%"
    def __repr__(self) -> str:
        return f"Percent(value={self.value})"
    def __hash__(self):
        return hash(self.value)