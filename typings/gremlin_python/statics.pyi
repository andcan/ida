from types import FunctionType as FunctionType
from typing import Any

class long(int): ...
FloatType = float
IntType = int
LongType = long
TypeType = type
ListType = list
DictType = dict
SetType = set
ByteBufferType = bytes

class timestamp(float): ...

class SingleByte(int):
    def __new__(cls, b: Any) -> None: ...

class SingleChar(str):
    def __new__(cls, c: Any) -> None: ...

class GremlinType:
    gremlin_type: Any = ...
    def __init__(self, gremlin_type: Any) -> None: ...

staticMethods: Any
staticEnums: Any
default_lambda_language: str

def add_static(key: Any, value: Any) -> None: ...
def load_statics(global_dict: Any) -> None: ...
def unload_statics(global_dict: Any) -> None: ...
