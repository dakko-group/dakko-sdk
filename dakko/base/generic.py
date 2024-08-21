from enum import Enum

# ----------------------- #


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        """Return a list of values from the enumeration."""

        return list(map(lambda c: c.value, cls))
