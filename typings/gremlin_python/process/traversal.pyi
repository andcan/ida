from .. import statics as statics
from ..statics import long as long
from typing import Any, Optional, Sequence

class Traversal:
    graph: Any = ...
    traversal_strategies: Any = ...
    bytecode: Any = ...
    side_effects: Any = ...
    traversers: Any = ...
    last_traverser: Any = ...
    def __init__(self, graph: Any, traversal_strategies: Any, bytecode: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __iter__(self) -> Any: ...
    def __next__(self): ...
    def toList(self) -> Sequence[Any]: ...
    def toSet(self): ...
    def iterate(self) -> Any: ...
    def nextTraverser(self): ...
    def hasNext(self) -> bool: ...
    def next(self, amount: Optional[Any] = ...) -> Any: ...
    def promise(self, cb: Optional[Any] = ...): ...

Barrier: Any
Cardinality: Any
Column: Any
Direction: Any
GraphSONVersion: Any
GryoVersion: Any
Order: Any
Pick: Any
Pop: Any
Scope: Any
T: Any
Operator: Any

class P:
    operator: Any = ...
    value: Any = ...
    other: Any = ...
    def __init__(self, operator: Any, value: Any, other: Optional[Any] = ...) -> None: ...
    @staticmethod
    def between(*args: Any): ...
    @staticmethod
    def eq(*args: Any): ...
    @staticmethod
    def gt(*args: Any): ...
    @staticmethod
    def gte(*args: Any): ...
    @staticmethod
    def inside(*args: Any): ...
    @staticmethod
    def lt(*args: Any): ...
    @staticmethod
    def lte(*args: Any): ...
    @staticmethod
    def neq(*args: Any): ...
    @staticmethod
    def not_(*args: Any): ...
    @staticmethod
    def outside(*args: Any): ...
    @staticmethod
    def test(*args: Any): ...
    @staticmethod
    def within(*args: Any): ...
    @staticmethod
    def without(*args: Any): ...
    def and_(self, arg: Any): ...
    def or_(self, arg: Any): ...
    def __eq__(self, other: Any) -> Any: ...

def between(*args: Any): ...
def eq(*args: Any): ...
def gt(*args: Any): ...
def gte(*args: Any): ...
def inside(*args: Any): ...
def lt(*args: Any): ...
def lte(*args: Any): ...
def neq(*args: Any): ...
def not_(*args: Any): ...
def outside(*args: Any): ...
def test(*args: Any): ...
def within(*args: Any): ...
def without(*args: Any): ...

class TextP(P):
    def __init__(self, operator: Any, value: Any, other: Optional[Any] = ...) -> None: ...
    @staticmethod
    def containing(*args: Any): ...
    @staticmethod
    def endingWith(*args: Any): ...
    @staticmethod
    def notContaining(*args: Any): ...
    @staticmethod
    def notEndingWith(*args: Any): ...
    @staticmethod
    def notStartingWith(*args: Any): ...
    @staticmethod
    def startingWith(*args: Any): ...
    def __eq__(self, other: Any) -> Any: ...

def containing(*args: Any): ...
def endingWith(*args: Any): ...
def notContaining(*args: Any): ...
def notEndingWith(*args: Any): ...
def notStartingWith(*args: Any): ...
def startingWith(*args: Any): ...

class IO:
    graphml: str = ...
    graphson: str = ...
    gryo: str = ...
    reader: str = ...
    registry: str = ...
    writer: str = ...

class ConnectedComponent:
    component: str = ...
    edges: str = ...
    propertyName: str = ...

class ShortestPath:
    distance: str = ...
    edges: str = ...
    includeEdges: str = ...
    maxDistance: str = ...
    target: str = ...

class PageRank:
    edges: str = ...
    propertyName: str = ...
    times: str = ...

class PeerPressure:
    edges: str = ...
    propertyName: str = ...
    times: str = ...

class Traverser:
    object: Any = ...
    bulk: Any = ...
    def __init__(self, object: Any, bulk: Optional[Any] = ...) -> None: ...
    def __eq__(self, other: Any) -> Any: ...

class TraversalSideEffects:
    def keys(self): ...
    def get(self, key: Any) -> None: ...
    def __getitem__(self, key: Any): ...

class TraversalStrategies:
    global_cache: Any = ...
    traversal_strategies: Any = ...
    def __init__(self, traversal_strategies: Optional[Any] = ...) -> None: ...
    def add_strategies(self, traversal_strategies: Any) -> None: ...
    def apply_strategies(self, traversal: Any) -> None: ...
    def apply_async_strategies(self, traversal: Any) -> None: ...

class TraversalStrategy:
    fqcn: Any = ...
    strategy_name: Any = ...
    configuration: Any = ...
    def __init__(self, strategy_name: Optional[Any] = ..., configuration: Optional[Any] = ..., fqcn: Optional[Any] = ...) -> None: ...
    def apply(self, traversal: Any) -> None: ...
    def apply_async(self, traversal: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...

class Bytecode:
    source_instructions: Any = ...
    step_instructions: Any = ...
    bindings: Any = ...
    def __init__(self, bytecode: Optional[Any] = ...) -> None: ...
    def add_source(self, source_name: Any, *args: Any) -> None: ...
    def add_step(self, step_name: Any, *args: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...

class Bindings:
    @staticmethod
    def of(key: Any, value: Any): ...

class Binding:
    key: Any = ...
    value: Any = ...
    def __init__(self, key: Any, value: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...

class WithOptions:
    tokens: str = ...
    none: int = ...
    ids: int = ...
    labels: int = ...
    keys: int = ...
    values: int = ...
    all: int = ...
    indexer: str = ...
    list: int = ...
    map: int = ...