from enum import Enum


class PythonToJsonschemaResponse200ArgsItemTypType0(str, Enum):
    STR = "str"
    FLOAT = "float"
    INT = "int"
    BOOL = "bool"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
