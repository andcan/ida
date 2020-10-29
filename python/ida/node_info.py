import yaml
from gremlin_python.driver import client
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


class NodeInfo:

    def __init__(self, label, properties):
        # type(str, PropertyInfo) -> None
        self.label = label
        self.properties = properties

    def __str__(self):
        string = '{0}{{'.format(self.label)
        for p in self.properties:
            string += '{0}'.format(p)
            if p != self.properties[-1]:
                string += ', '
        string += '}'
        return string

    def to_dict(self):
        # type () -> dict[str, Any]
        return {
            'label': self.label,
            'properties': map(lambda e: e.to_dict(), self.properties),
        }

    @classmethod
    def from_dict(cls, data):
        return NodeInfo(label=data['label'], properties=map(lambda e: PropertyInfo.from_dict(e), data['properties']))

    @classmethod
    def from_result(cls, result):
        xs = []
        for label in result:
            properties = []
            node_data = result[label]
            for prop in node_data:
                prop_data = node_data[prop]
                properties.append(PropertyInfo(prop, prop_data['@value'].replace('java.lang.', '')))
            xs.append(NodeInfo(label, properties))
        return xs


class PropertyInfo:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.kind)

    def to_dict(self):
        return {
            'name': self.name,
            'kind': self.kind,
        }

    @classmethod
    def from_dict(cls, data):
        return PropertyInfo(name=data['name'], kind=data['kind'])


def main():
    connection = DriverRemoteConnection('ws://localhost:8182/gremlin', '{0}_traversal'.format('bandi'))
    # g = traversal().withRemote(connection)

    c = client.Client('ws://localhost:8182/gremlin', '{0}_traversal'.format('bandi'))

    results = c.submit(
        'g.V().group().by(label).by(properties().group().by(key).by(value().map{it.get().getClass()}))'
    ).all().result()
    nodes_info = NodeInfo.from_result(results[0])

    encoded = yaml.safe_dump({'nodes': map(lambda e: e.to_dict(), nodes_info)})
    print(encoded)
    print(NodeInfo.from_dict(yaml.safe_load(encoded)))
    connection.close()


if __name__ == '__main__':
    main()
