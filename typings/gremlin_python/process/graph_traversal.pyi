from .. import statics as statics
from ..driver.remote_connection import RemoteStrategy as RemoteStrategy
from ..statics import long as long
from .strategies import VertexProgramStrategy as VertexProgramStrategy
from .traversal import Bytecode as Bytecode, Traversal as Traversal, TraversalStrategies as TraversalStrategies
from typing import Any, Optional


class GraphTraversalSource:
    graph: Any = ...
    traversal_strategies: Any = ...
    bytecode: Any = ...
    graph_traversal: Any = ...
    def __init__(self, graph: Any, traversal_strategies: Any, bytecode: Optional[Any] = ...) -> None: ...
    def get_graph_traversal_source(self): ...
    def get_graph_traversal(self): ...
    def withBulk(self, *args: Any): ...
    def withPath(self, *args: Any): ...
    def withSack(self, *args: Any): ...
    def withSideEffect(self, *args: Any): ...
    def withStrategies(self, *args: Any): ...
    def with_(self, *args: Any): ...
    def withoutStrategies(self, *args: Any): ...
    def withRemote(self, remote_connection: Any): ...
    def withComputer(self, graph_computer: Optional[Any] = ..., workers: Optional[Any] = ..., result: Optional[Any] = ..., persist: Optional[Any] = ..., vertices: Optional[Any] = ..., edges: Optional[Any] = ..., configuration: Optional[Any] = ...): ...
    def E(self, *args: Any): ...
    def V(self, *args: Any) -> GraphTraversal: ...
    def addE(self, *args: Any): ...
    def addV(self, *args: Any): ...
    def inject(self, *args: Any): ...
    def io(self, *args: Any): ...


class GraphTraversal(Traversal):
    def __init__(self, graph: Any, traversal_strategies: Any, bytecode: Any) -> None: ...
    def __getitem__(self, index: Any): ...
    def __getattr__(self, key: Any): ...
    def clone(self): ...
    def V(self, *args: Any) -> GraphTraversal: ...
    def addE(self, *args: Any) -> GraphTraversal: ...
    def addV(self, *args: Any) -> GraphTraversal: ...
    def aggregate(self, *args: Any) -> GraphTraversal: ...
    def and_(self, *args: Any) -> GraphTraversal: ...
    def as_(self, *args: Any) -> GraphTraversal: ...
    def barrier(self, *args: Any) -> GraphTraversal: ...
    def both(self, *args: Any) -> GraphTraversal: ...
    def bothE(self, *args: Any) -> GraphTraversal: ...
    def bothV(self, *args: Any) -> GraphTraversal: ...
    def branch(self, *args: Any) -> GraphTraversal: ...
    def by(self, *args: Any) -> GraphTraversal: ...
    def cap(self, *args: Any) -> GraphTraversal: ...
    def choose(self, *args: Any) -> GraphTraversal: ...
    def coalesce(self, *args: Any) -> GraphTraversal: ...
    def coin(self, *args: Any) -> GraphTraversal: ...
    def connectedComponent(self, *args: Any) -> GraphTraversal: ...
    def constant(self, *args: Any) -> GraphTraversal: ...
    def count(self, *args: Any) -> GraphTraversal: ...
    def cyclicPath(self, *args: Any) -> GraphTraversal: ...
    def dedup(self, *args: Any) -> GraphTraversal: ...
    def drop(self, *args: Any) -> GraphTraversal: ...
    def elementMap(self, *args: Any) -> GraphTraversal: ...
    def emit(self, *args: Any) -> GraphTraversal: ...
    def filter_(self, *args: Any) -> GraphTraversal: ...
    def flatMap(self, *args: Any) -> GraphTraversal: ...
    def fold(self, *args: Any) -> GraphTraversal: ...
    def from_(self, *args: Any) -> GraphTraversal: ...
    def group(self, *args: Any) -> GraphTraversal: ...
    def groupCount(self, *args: Any) -> GraphTraversal: ...
    def has(self, *args: Any) -> GraphTraversal: ...
    def hasId(self, *args: Any) -> GraphTraversal: ...
    def hasKey(self, *args: Any) -> GraphTraversal: ...
    def hasLabel(self, *args: Any) -> GraphTraversal: ...
    def hasNot(self, *args: Any) -> GraphTraversal: ...
    def hasValue(self, *args: Any) -> GraphTraversal: ...
    def id_(self, *args: Any) -> GraphTraversal: ...
    def identity(self, *args: Any) -> GraphTraversal: ...
    def inE(self, *args: Any) -> GraphTraversal: ...
    def inV(self, *args: Any) -> GraphTraversal: ...
    def in_(self, *args: Any) -> GraphTraversal: ...
    def index(self, *args: Any) -> GraphTraversal: ...
    def inject(self, *args: Any) -> GraphTraversal: ...
    def is_(self, *args: Any) -> GraphTraversal: ...
    def key(self, *args: Any) -> GraphTraversal: ...
    def label(self, *args: Any) -> GraphTraversal: ...
    def limit(self, *args: Any) -> GraphTraversal: ...
    def local(self, *args: Any) -> GraphTraversal: ...
    def loops(self, *args: Any) -> GraphTraversal: ...
    def map(self, *args: Any) -> GraphTraversal: ...
    def match(self, *args: Any) -> GraphTraversal: ...
    def math(self, *args: Any) -> GraphTraversal: ...
    def max_(self, *args: Any) -> GraphTraversal: ...
    def mean(self, *args: Any) -> GraphTraversal: ...
    def min_(self, *args: Any) -> GraphTraversal: ...
    def not_(self, *args: Any) -> GraphTraversal: ...
    def option(self, *args: Any) -> GraphTraversal: ...
    def optional(self, *args: Any) -> GraphTraversal: ...
    def or_(self, *args: Any) -> GraphTraversal: ...
    def order(self, *args: Any) -> GraphTraversal: ...
    def otherV(self, *args: Any) -> GraphTraversal: ...
    def out(self, *args: Any) -> GraphTraversal: ...
    def outE(self, *args: Any) -> GraphTraversal: ...
    def outV(self, *args: Any) -> GraphTraversal: ...
    def pageRank(self, *args: Any) -> GraphTraversal: ...
    def path(self, *args: Any) -> GraphTraversal: ...
    def peerPressure(self, *args: Any) -> GraphTraversal: ...
    def profile(self, *args: Any) -> GraphTraversal: ...
    def program(self, *args: Any) -> GraphTraversal: ...
    def project(self, *args: Any) -> GraphTraversal: ...
    def properties(self, *args: Any) -> GraphTraversal: ...
    def property(self, *args: Any) -> GraphTraversal: ...
    def propertyMap(self, *args: Any) -> GraphTraversal: ...
    def range_(self, *args: Any) -> GraphTraversal: ...
    def read(self, *args: Any) -> GraphTraversal: ...
    def repeat(self, *args: Any) -> GraphTraversal: ...
    def sack(self, *args: Any) -> GraphTraversal: ...
    def sample(self, *args: Any) -> GraphTraversal: ...
    def select(self, *args: Any) -> GraphTraversal: ...
    def shortestPath(self, *args: Any) -> GraphTraversal: ...
    def sideEffect(self, *args: Any) -> GraphTraversal: ...
    def simplePath(self, *args: Any) -> GraphTraversal: ...
    def skip(self, *args: Any) -> GraphTraversal: ...
    def store(self, *args: Any) -> GraphTraversal: ...
    def subgraph(self, *args: Any) -> GraphTraversal: ...
    def sum_(self, *args: Any) -> GraphTraversal: ...
    def tail(self, *args: Any) -> GraphTraversal: ...
    def timeLimit(self, *args: Any) -> GraphTraversal: ...
    def times(self, *args: Any) -> GraphTraversal: ...
    def to(self, *args: Any) -> GraphTraversal: ...
    def toE(self, *args: Any) -> GraphTraversal: ...
    def toV(self, *args: Any) -> GraphTraversal: ...
    def tree(self, *args: Any) -> GraphTraversal: ...
    def unfold(self, *args: Any) -> GraphTraversal: ...
    def union(self, *args: Any) -> GraphTraversal: ...
    def until(self, *args: Any) -> GraphTraversal: ...
    def value(self, *args: Any) -> GraphTraversal: ...
    def valueMap(self, *args: Any) -> GraphTraversal: ...
    def values(self, *args: Any) -> GraphTraversal: ...
    def where(self, *args: Any) -> GraphTraversal: ...
    def with_(self, *args: Any) -> GraphTraversal: ...
    def write(self, *args: Any) -> GraphTraversal: ...
    def filter(self, *args: Any) -> GraphTraversal: ...
    def id(self, *args: Any) -> GraphTraversal: ...
    def max(self, *args: Any) -> GraphTraversal: ...
    def min(self, *args: Any) -> GraphTraversal: ...
    def range(self, *args: Any) -> GraphTraversal: ...
    def sum(self, *args: Any) -> GraphTraversal: ...


class __:
    graph_traversal: Any = ...
    @classmethod
    def start(cls) -> GraphTraversal: ...
    @classmethod
    def __(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def V(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def addE(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def addV(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def aggregate(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def and_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def as_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def barrier(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def both(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def bothE(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def bothV(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def branch(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def cap(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def choose(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def coalesce(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def coin(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def constant(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def count(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def cyclicPath(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def dedup(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def drop(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def elementMap(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def emit(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def filter_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def flatMap(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def fold(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def group(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def groupCount(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def has(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def hasId(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def hasKey(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def hasLabel(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def hasNot(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def hasValue(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def id_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def identity(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def inE(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def inV(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def in_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def index(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def inject(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def is_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def key(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def label(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def limit(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def local(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def loops(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def map(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def match(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def math(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def max_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def mean(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def min_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def not_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def optional(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def or_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def order(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def otherV(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def out(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def outE(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def outV(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def path(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def project(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def properties(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def property(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def propertyMap(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def range_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def repeat(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def sack(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def sample(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def select(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def sideEffect(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def simplePath(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def skip(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def store(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def subgraph(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def sum_(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def tail(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def timeLimit(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def times(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def to(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def toE(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def toV(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def tree(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def unfold(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def union(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def until(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def value(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def valueMap(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def values(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def where(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def filter(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def id(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def max(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def min(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def range(cls, *args: Any) -> GraphTraversal: ...
    @classmethod
    def sum(cls, *args: Any) -> GraphTraversal: ...


def V(*args: Any) -> GraphTraversal: ...
def addE(*args: Any) -> GraphTraversal: ...
def addV(*args: Any) -> GraphTraversal: ...
def aggregate(*args: Any) -> GraphTraversal: ...
def and_(*args: Any) -> GraphTraversal: ...
def as_(*args: Any) -> GraphTraversal: ...
def barrier(*args: Any) -> GraphTraversal: ...
def both(*args: Any) -> GraphTraversal: ...
def bothE(*args: Any) -> GraphTraversal: ...
def bothV(*args: Any) -> GraphTraversal: ...
def branch(*args: Any) -> GraphTraversal: ...
def cap(*args: Any) -> GraphTraversal: ...
def choose(*args: Any) -> GraphTraversal: ...
def coalesce(*args: Any) -> GraphTraversal: ...
def coin(*args: Any) -> GraphTraversal: ...
def constant(*args: Any) -> GraphTraversal: ...
def count(*args: Any) -> GraphTraversal: ...
def cyclicPath(*args: Any) -> GraphTraversal: ...
def dedup(*args: Any) -> GraphTraversal: ...
def drop(*args: Any) -> GraphTraversal: ...
def elementMap(*args: Any) -> GraphTraversal: ...
def emit(*args: Any) -> GraphTraversal: ...
def filter_(*args: Any) -> GraphTraversal: ...
def flatMap(*args: Any) -> GraphTraversal: ...
def fold(*args: Any) -> GraphTraversal: ...
def group(*args: Any) -> GraphTraversal: ...
def groupCount(*args: Any) -> GraphTraversal: ...
def has(*args: Any) -> GraphTraversal: ...
def hasId(*args: Any) -> GraphTraversal: ...
def hasKey(*args: Any) -> GraphTraversal: ...
def hasLabel(*args: Any) -> GraphTraversal: ...
def hasNot(*args: Any) -> GraphTraversal: ...
def hasValue(*args: Any) -> GraphTraversal: ...
def id_(*args: Any) -> GraphTraversal: ...
def identity(*args: Any) -> GraphTraversal: ...
def inE(*args: Any) -> GraphTraversal: ...
def inV(*args: Any) -> GraphTraversal: ...
def in_(*args: Any) -> GraphTraversal: ...
def index(*args: Any) -> GraphTraversal: ...
def inject(*args: Any) -> GraphTraversal: ...
def is_(*args: Any) -> GraphTraversal: ...
def key(*args: Any) -> GraphTraversal: ...
def label(*args: Any) -> GraphTraversal: ...
def limit(*args: Any) -> GraphTraversal: ...
def local(*args: Any) -> GraphTraversal: ...
def loops(*args: Any) -> GraphTraversal: ...
def map(*args: Any) -> GraphTraversal: ...
def match(*args: Any) -> GraphTraversal: ...
def math(*args: Any) -> GraphTraversal: ...
def max_(*args: Any) -> GraphTraversal: ...
def mean(*args: Any) -> GraphTraversal: ...
def min_(*args: Any) -> GraphTraversal: ...
def not_(*args: Any) -> GraphTraversal: ...
def optional(*args: Any) -> GraphTraversal: ...
def or_(*args: Any) -> GraphTraversal: ...
def order(*args: Any) -> GraphTraversal: ...
def otherV(*args: Any) -> GraphTraversal: ...
def out(*args: Any) -> GraphTraversal: ...
def outE(*args: Any) -> GraphTraversal: ...
def outV(*args: Any) -> GraphTraversal: ...
def path(*args: Any) -> GraphTraversal: ...
def project(*args: Any) -> GraphTraversal: ...
def properties(*args: Any) -> GraphTraversal: ...
def property(*args: Any) -> GraphTraversal: ...
def propertyMap(*args: Any) -> GraphTraversal: ...
def range_(*args: Any) -> GraphTraversal: ...
def repeat(*args: Any) -> GraphTraversal: ...
def sack(*args: Any) -> GraphTraversal: ...
def sample(*args: Any) -> GraphTraversal: ...
def select(*args: Any) -> GraphTraversal: ...
def sideEffect(*args: Any) -> GraphTraversal: ...
def simplePath(*args: Any) -> GraphTraversal: ...
def skip(*args: Any) -> GraphTraversal: ...
def store(*args: Any) -> GraphTraversal: ...
def subgraph(*args: Any) -> GraphTraversal: ...
def sum_(*args: Any) -> GraphTraversal: ...
def tail(*args: Any) -> GraphTraversal: ...
def timeLimit(*args: Any) -> GraphTraversal: ...
def times(*args: Any) -> GraphTraversal: ...
def to(*args: Any) -> GraphTraversal: ...
def toE(*args: Any) -> GraphTraversal: ...
def toV(*args: Any) -> GraphTraversal: ...
def tree(*args: Any) -> GraphTraversal: ...
def unfold(*args: Any) -> GraphTraversal: ...
def union(*args: Any) -> GraphTraversal: ...
def until(*args: Any) -> GraphTraversal: ...
def value(*args: Any) -> GraphTraversal: ...
def valueMap(*args: Any) -> GraphTraversal: ...
def values(*args: Any) -> GraphTraversal: ...
def where(*args: Any) -> GraphTraversal: ...
def filter(*args: Any) -> GraphTraversal: ...
def id(*args: Any) -> GraphTraversal: ...
def max(*args: Any) -> GraphTraversal: ...
def min(*args: Any) -> GraphTraversal: ...
def range(*args: Any) -> GraphTraversal: ...
def sum(*args: Any) -> GraphTraversal: ...
