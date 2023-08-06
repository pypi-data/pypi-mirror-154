# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Degree:
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

    def __repr__(self) -> str:
        return f"Degree(value={self.value})"
    def __hash__(self):
        return hash(self.value)