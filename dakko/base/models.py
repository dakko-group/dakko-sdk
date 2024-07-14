from enum import Enum

from pydantic import BaseModel, ConfigDict

# ----------------------- #


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        """Return a list of values from the enumeration."""

        return list(map(lambda c: c.value, cls))


# ----------------------- #


class BaseModelEnum(BaseModel):

    model_config = ConfigDict(
        use_enum_values=True,
        validate_default=True,
    )
