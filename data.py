from typing import Any, Dict, List, Optional, Sequence
from attr import attrs

import related

merge_always = 'merge_always'
merge_if_not_present = 'merge_if_not_present'


@related.immutable()
class PropertySchema(object):
    name = related.StringField()
    kind = related.StringField()

    def __init__(
        self,
        name,  # type: str
        kind,  # type: str
    ):
        super(PropertySchema, self).__init__(
            name=name,  # type: ignore
            kind=kind,  # type: ignore
        )

    def to_dict(self):
        # type: () -> Dict[str, Any]
        return related.to_dict(self)

    def to_yaml(self):
        # type: () -> str
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> PropertySchema
        return related.to_model(cls, value)


@related.immutable()
class NodeSchema(object):
    label = related.StringField()
    properties = related.SequenceField(PropertySchema, repr=True)

    def __init__(
        self,
        label,  # type: str
        properties,  # type: Sequence[PropertySchema]
    ):
        super(NodeSchema, self).__init__(
            label=label,  # type: ignore
            properties=properties,  # type: ignore
        )

    def to_dict(self):
        # type: () -> Dict[str, Any]
        return related.to_dict(self)

    def to_yaml(self):
        # type: () -> str
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> NodeSchema
        return related.to_model(NodeSchema, value)

    def property_by_name(self, name):
        # type: (str) -> Optional[PropertySchema]
        for property in self.properties:
            if property.name == name:
                return property
        return None


@related.immutable()
class Schema(object):
    nodes = related.SequenceField(NodeSchema, repr=True)

    def __init__(
        self,
        nodes,  # type: Sequence[NodeSchema]
    ):
        super(Schema, self).__init__(
            nodes=nodes,  # type: ignore
        )

    def to_dict(self):
        # type: () -> Dict[str, Any]
        return related.to_dict(self)

    def to_yaml(self):
        # type: () -> str
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> Schema
        return related.to_model(Schema, value)

    def node_by_label(self, label):
        # type: (str) -> Optional[NodeSchema]
        for node in self.nodes:
            if node.label == label:
                return node
        return None


@related.immutable()
class KeyMapping(object):
    name = related.StringField()

    def __init__(
        self,
        name,  # type: str
    ):
        super(KeyMapping, self).__init__(
            name=name,  # type: ignore
        )

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


@related.immutable()
class PropertyMapping(object):
    name = related.StringField()
    source = related.StringField()
    merge_behavior = related.StringField(required=False)

    def __init__(
        self,
        name,  # type: str
        source,  # type: str
        merge_behavior=None,  # type: Optional[str]
    ):
        super(PropertyMapping, self).__init__(
            name=name,  # type: ignore
            source=source,  # type: ignore
            merge_behavior=merge_behavior,  # type: ignore
        )

    def to_dict(self):
        # type: () -> Dict[str, Any]
        return related.to_dict(self)

    def to_yaml(self):
        # type: () -> str
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> PropertyMapping
        return related.to_model(PropertyMapping, value)


def immutable_mapping(maybe_cls=None, strict=False):

    def wrap(cls):
        cls.relations = related.SequenceField(cls, repr=True, required=False)
        wrapped = attrs(cls, frozen=True, slots=True)
        wrapped.__related_strict__ = strict
        return wrapped

    return wrap(maybe_cls) if maybe_cls is not None else wrap


@immutable_mapping()
class Mapping(object):
    name = related.StringField()
    label = related.StringField()
    keys = related.SequenceField(KeyMapping, repr=True)
    properties = related.SequenceField(PropertyMapping, repr=True)

    def __init__(
        self,
        label,  # type: str
        name,  # type: str
        keys,  # type: Sequence[KeyMapping]
        properties,  # type: Sequence[PropertyMapping]
        relations,  # type: Sequence[Mapping]
    ):
        self.relations = related.SequenceField(Mapping, repr=True)
        super(Mapping, self).__init__(
            label=label,  # type: ignore
            name=name,  # type: ignore
            keys=keys,  # type: ignore
            properties=properties,  # type: ignore
            relations=relations,  # type: ignore
        )

    def is_key_property(self, property):
        # type: (PropertyMapping) -> bool
        for k in self.keys:
            if k.name == property.name:
                return True
        return False

    def key_properties(self):
        ps = []  # type: Sequence[PropertyMapping]
        for property in self.properties:
            if self.is_key_property(property):
                ps.append(property)
        return ps

    def non_key_properties(self):
        ps = []  # type: Sequence[PropertyMapping]
        for property in self.properties:
            if not self.is_key_property(property):
                ps.append(property)
        return ps

    def property_by_key(self, key):
        # type: (KeyMapping) -> Optional[PropertyMapping]
        for p in self.properties:
            if p.name == key.name:
                return p
        return None

    def property_by_source(self, source):
        # type: (str) -> Optional[PropertyMapping]
        for p in self.properties:
            if p.source == source:
                return p
        return None

    def to_dict(self):
        # type: () -> Dict[str, Any]
        return related.to_dict(self)

    def to_yaml(self):
        # type: () -> str
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> Mapping
        return related.to_model(Mapping, value)
