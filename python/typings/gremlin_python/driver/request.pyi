from collections import namedtuple

RequestMessage = namedtuple('RequestMessage', ['processor', 'op', 'args'])
