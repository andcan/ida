from __future__ import annotations
from typing import Any, Dict, List, Optional, Sequence

import related
import itertools

merge_always = 'merge_always'
merge_if_not_present = 'merge_if_not_present'


@related.mutable()
class PropertySchema(object):
    name = related.StringField()
    kind = related.StringField()

    def __init__(
        self,
        name: str,
        kind: str,
    ):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return related.to_dict(self)

    def to_yaml(self) -> str:
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> PropertySchema:
        return related.to_model(cls, value)


@related.mutable()
class NodeSchema(object):
    label = related.StringField()
    properties = related.SequenceField(PropertySchema, repr=True)

    def __init__(
        self,
        label: str,
        properties: Sequence[PropertySchema],
    ):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return related.to_dict(self)

    def to_yaml(self) -> str:
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> NodeSchema:
        return related.to_model(NodeSchema, value)

    def property_by_name(self, name: str) -> Optional[PropertySchema]:
        for property in self.properties:
            if property.name == name:
                return property
        return None


@related.mutable()
class Schema(object):
    nodes = related.SequenceField(NodeSchema, repr=True)

    def __init__(
        self,
        nodes: Sequence[NodeSchema],
    ):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return related.to_dict(self)

    def to_yaml(self) -> str:
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> Schema:
        return related.to_model(Schema, value)

    def node_by_label(self, label: str) -> Optional[NodeSchema]:
        for node in self.nodes:
            if node.label == label:
                return node
        return None


@related.mutable()
class KeyMapping(object):
    name = related.StringField()

    def __init__(
        self,
        name,  # type: str
    ):
        pass

    def to_dict(self):
        # type: () -> Dict[str, Any]
        return related.to_dict(self)

    def to_yaml(self):
        # type: () -> str
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> KeyMapping
        return related.to_model(KeyMapping, value)


@related.mutable()
class PropertyMapping(object):
    name = related.StringField()
    source = related.StringField()
    merge_behavior = related.StringField(
        required=False,
        default=merge_if_not_present
    )
    kind = related.StringField(
        required=False,
    )
    format = related.StringField(
        required=False,
    )
    is_edge_property = related.BooleanField(
        default=False,
    )

    def __init__(
        self,
        name: str,
        source: str,
        merge_behavior: Optional[str] = None,
        kind: Optional[str] = None,
        format: Optional[str] = None,
    ):
        pass

    def to_dict(self) -> Dict[str, Any]:
        return related.to_dict(self)

    def to_yaml(self) -> str:
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> PropertyMapping
        return related.to_model(PropertyMapping, value)


@related.mutable()
class Mapping(object):
    name = related.StringField()
    label = related.StringField()
    keys = related.SequenceField(KeyMapping, repr=True)
    properties = related.SequenceField(PropertyMapping, repr=True)
    edge_keys = related.SequenceField(KeyMapping, repr=True, default=[])
    edge_properties = related.SequenceField(
        KeyMapping,
        repr=True,
        default=[],
    )
    relations = related.SequenceField(
        'data.Mapping',
        repr=True,
        default=[],
    )

    def __init__(
        self,
        label: str,
        name: str,
        keys: Sequence[KeyMapping],
        edge_keys: Sequence[KeyMapping],
        edge_properties: Sequence[KeyMapping],
        properties: Sequence[PropertyMapping],
        relations: Optional[Sequence[Dict[str, Any]]] = None,
    ):
        pass

    def edge_key_properties(self, relation: Mapping) -> Sequence[PropertyMapping]:
        ps = []
        for property in self.properties:
            if self.is_edge_key_property(relation, property):
                ps.append(property)
        return ps

    def is_key_property(self, property: PropertyMapping) -> bool:
        for k in self.keys:
            if k.name == property.name:
                return True
        return False

    def is_edge_property(self, relation: Mapping, property: PropertyMapping) -> bool:
        for k in relation.edge_properties:
            if k.name == property.name:
                return True
        return False

    def is_edge_key_property(self, relation: Mapping, property: PropertyMapping) -> bool:
        for k in relation.edge_keys:
            if k.name == property.name:
                return True
        return False

    def key_properties(self) -> Sequence[PropertyMapping]:
        ps = []
        for property in self.properties:
            if self.is_key_property(property):
                ps.append(property)
        return ps

    def non_key_properties(self) -> Sequence[PropertyMapping]:
        ps = []
        for property in self.properties:
            if not self.is_key_property(property):
                ps.append(property)
        return ps

    def property_by_key(self, key: KeyMapping) -> Optional[PropertyMapping]:
        for p in self.properties:
            if p.name == key.name:
                return p
        return None

    def property_by_source(self, source: str) -> Optional[PropertyMapping]:
        for p in self.properties:
            if p.source == source:
                return p
        return None

    def to_dict(self) -> Dict[str, Any]:
        return related.to_dict(self)

    def to_yaml(self) -> str:
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> Mapping:
        return related.to_model(Mapping, value)
