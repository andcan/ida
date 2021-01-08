from decimal import *
from gremlin_python import statics as statics
from gremlin_python.process.traversal import Binding as Binding, Bytecode as Bytecode, P as P, TextP as TextP, Traversal as Traversal, TraversalStrategy as TraversalStrategy, Traverser as Traverser
from gremlin_python.statics import ByteBufferType as ByteBufferType, FloatType as FloatType, FunctionType as FunctionType, IntType as IntType, LongType as LongType, SingleByte as SingleByte, SingleChar as SingleChar, TypeType as TypeType
from gremlin_python.structure.graph import Edge as Edge, Path as Path, Property as Property, Vertex as Vertex, VertexProperty as VertexProperty
from typing import Any, Optional

class GraphSONTypeType(type):
    def __new__(mcs: Any, name: Any, bases: Any, dct: Any): ...

class GraphSONUtil:
    TYPE_KEY: str = ...
    VALUE_KEY: str = ...
    @classmethod
    def typedValue(cls, type_name: Any, value: Any, prefix: str = ...): ...
    @classmethod
    def formatType(cls, prefix: Any, type_name: Any): ...

class GraphSONWriter:
    serializers: Any = ...
    def __init__(self, serializer_map: Optional[Any] = ...) -> None: ...
    def writeObject(self, objectData: Any): ...
    def toDict(self, obj: Any): ...

class GraphSONReader:
    deserializers: Any = ...
    def __init__(self, deserializer_map: Optional[Any] = ...) -> None: ...
    def readObject(self, jsonData: Any): ...
    def toObject(self, obj: Any): ...

class _GraphSONTypeIO(metaclass=GraphSONTypeType):
    python_type: Any = ...
    graphson_type: Any = ...
    symbolMap: Any = ...
    @classmethod
    def unmangleKeyword(cls, symbol: Any): ...
    def dictify(self, obj: Any, writer: Any) -> None: ...
    def objectify(self, d: Any, reader: Any) -> None: ...

class _BytecodeSerializer(_GraphSONTypeIO):
    @classmethod
    def dictify(cls, bytecode: Any, writer: Any): ...

class TraversalSerializer(_BytecodeSerializer):
    python_type: Any = ...

class BytecodeSerializer(_BytecodeSerializer):
    python_type: Any = ...

class VertexSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    @classmethod
    def dictify(cls, vertex: Any, writer: Any): ...

class EdgeSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    @classmethod
    def dictify(cls, edge: Any, writer: Any): ...

class VertexPropertySerializer(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    @classmethod
    def dictify(cls, vertex_property: Any, writer: Any): ...

class PropertySerializer(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    @classmethod
    def dictify(cls, property: Any, writer: Any): ...

class TraversalStrategySerializer(_GraphSONTypeIO):
    python_type: Any = ...
    @classmethod
    def dictify(cls, strategy: Any, writer: Any): ...

class TraverserIO(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    @classmethod
    def dictify(cls, traverser: Any, writer: Any): ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class EnumSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    @classmethod
    def dictify(cls, enum: Any, _: Any): ...

class PSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    @classmethod
    def dictify(cls, p: Any, writer: Any): ...

class TextPSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    @classmethod
    def dictify(cls, p: Any, writer: Any): ...

class BindingSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    @classmethod
    def dictify(cls, binding: Any, writer: Any): ...

class LambdaSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    @classmethod
    def dictify(cls, lambda_object: Any, writer: Any): ...

class TypeSerializer(_GraphSONTypeIO):
    python_type: Any = ...
    @classmethod
    def dictify(cls, typ: Any, writer: Any): ...

class UUIDIO(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, obj: Any, writer: Any): ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class DateIO(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, obj: Any, writer: Any): ...
    @classmethod
    def objectify(cls, ts: Any, reader: Any): ...

class TimestampIO(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, obj: Any, writer: Any): ...
    @classmethod
    def objectify(cls, ts: Any, reader: Any): ...

class _NumberIO(_GraphSONTypeIO):
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...
    @classmethod
    def objectify(cls, v: Any, _: Any): ...

class FloatIO(_NumberIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...
    @classmethod
    def objectify(cls, v: Any, _: Any): ...

class BigDecimalIO(_NumberIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...
    @classmethod
    def objectify(cls, v: Any, _: Any): ...

class DoubleIO(FloatIO):
    graphson_type: str = ...
    graphson_base_type: str = ...

class Int64IO(_NumberIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...

class BigIntegerIO(Int64IO):
    graphson_type: str = ...

class Int32IO(Int64IO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...

class ByteIO(_NumberIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...
    @classmethod
    def objectify(cls, v: Any, _: Any): ...

class ByteBufferIO(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...
    @classmethod
    def objectify(cls, v: Any, _: Any): ...

class CharIO(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...
    @classmethod
    def objectify(cls, v: Any, _: Any): ...

class DurationIO(_GraphSONTypeIO):
    python_type: Any = ...
    graphson_type: str = ...
    graphson_base_type: str = ...
    @classmethod
    def dictify(cls, n: Any, writer: Any): ...
    @classmethod
    def objectify(cls, v: Any, _: Any): ...

class VertexDeserializer(_GraphSONTypeIO):
    graphson_type: str = ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class EdgeDeserializer(_GraphSONTypeIO):
    graphson_type: str = ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class VertexPropertyDeserializer(_GraphSONTypeIO):
    graphson_type: str = ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class PropertyDeserializer(_GraphSONTypeIO):
    graphson_type: str = ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class PathDeserializer(_GraphSONTypeIO):
    graphson_type: str = ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class TraversalMetricsDeserializer(_GraphSONTypeIO):
    graphson_type: str = ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...

class MetricsDeserializer(_GraphSONTypeIO):
    graphson_type: str = ...
    @classmethod
    def objectify(cls, d: Any, reader: Any): ...