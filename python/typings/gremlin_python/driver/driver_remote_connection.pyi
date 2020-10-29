from gremlin_python.driver import client as client, serializer as serializer
from gremlin_python.driver.remote_connection import RemoteConnection as RemoteConnection, RemoteTraversal as RemoteTraversal, RemoteTraversalSideEffects as RemoteTraversalSideEffects
from typing import Any, Optional

class DriverRemoteConnection(RemoteConnection):
    def __init__(self, url: Any, traversal_source: Any, protocol_factory: Optional[Any] = ..., transport_factory: Optional[Any] = ..., pool_size: Optional[Any] = ..., max_workers: Optional[Any] = ..., username: str = ..., password: str = ..., message_serializer: Optional[Any] = ..., graphson_reader: Optional[Any] = ..., graphson_writer: Optional[Any] = ..., headers: Optional[Any] = ...) -> None: ...
    def close(self) -> None: ...
    def submit(self, bytecode: Any): ...
    def submitAsync(self, bytecode: Any): ...
