from typing import Annotated, Dict, Literal, TypeAlias

# ----------------------- #

# Annotations
FieldName = Annotated[str, "The name of the data model field"]
FieldTitle = Annotated[str, "The title of the data model field"]
FieldDataType = Annotated[str, "The data type of the data model field"]

Field = Annotated[
    Dict[str, FieldName | FieldTitle | FieldDataType], "The data model field"
]

# Aliases
Wildcard: TypeAlias = Literal["*", "all"]
