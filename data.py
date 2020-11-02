from typing import Any, Dict

import related


@related.immutable
class PropertySchema(object):
    name = related.StringField()
    kind = related.StringField()

    def to_dict(self):
        return related.to_dict(self)

    def to_yaml(self):
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> PropertySchema
        return related.to_model(cls, value)


@related.immutable
class NodeSchema(object):
    label = related.StringField()
    properties = related.SequenceField(PropertySchema)

    def to_dict(self):
        return related.to_dict(self)

    def to_yaml(self):
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> NodeSchema
        return related.to_model(NodeSchema, value)


@related.immutable
class FieldMapping(object):
    source = related.StringField()
    destination = related.StringField()

    def to_dict(self):
        return related.to_dict(self)

    def to_yaml(self):
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> FieldMapping
        return related.to_model(FieldMapping, value)


@related.immutable
class Mapping(object):
    node = related.StringField()
    properties = related.SequenceField(FieldMapping)

    def to_dict(self):
        return related.to_dict(self)

    def to_yaml(self):
        return related.to_yaml(self.to_dict())

    @classmethod
    def from_dict(cls, value):
        # type: (Dict[str, Any]) -> Mapping
        return related.to_model(Mapping, value)
