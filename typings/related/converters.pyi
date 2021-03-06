"""
This type stub file was generated by pyright.
"""

CHILD_ERROR_MSG = "Failed to convert value ({}) to child object class ({}). " + "... [Original error message: {}]"
def to_child_field(cls):
    """
    Returns an callable instance that will convert a value to a Child object.

    :param cls: Valid class type of the Child.
    :return: instance of ChildConverter.
    """
    class ChildConverter(object):
        ...
    
    

def to_sequence_field(cls):
    """
    Returns a callable instance that will convert a value to a Sequence.

    :param cls: Valid class type of the items in the Sequence.
    :return: instance of the SequenceConverter.
    """
    class SequenceConverter(object):
        ...
    
    

def to_set_field(cls):
    """
    Returns a callable instance that will convert a value to a Sequence.

    :param cls: Valid class type of the items in the Sequence.
    :return: instance of the SequenceConverter.
    """
    class SetConverter(object):
        ...
    
    

def to_mapping_field(cls, key):
    """
    Returns a callable instance that will convert a value to a Mapping.

    :param cls: Valid class type of the items in the Sequence.
    :param key: Attribute name of the key value in each item of cls instance.
    :return: instance of the MappingConverter.
    """
    class MappingConverter(object):
        ...
    
    

def str_if_not_none(value):
    """
    Returns an str(value) if the value is not None.

    :param value: None or a value that can be converted to a str.
    :return: None or str(value)
    """
    ...

def int_if_not_none(value):
    """
    Returns an int(value) if the value is not None.

    :param value: None or a value that can be converted to an int.
    :return: None or int(value)
    """
    ...

def float_if_not_none(value):
    """
    Returns an float(value) if the value is not None.

    :param value: None or a value that can be converted to an float.
    :return: None or float(value)
    """
    ...

def str_to_url(value):
    """
    Returns a UUID(value) if the value provided is a str.

    :param value: str or UUID object
    :return: UUID object
    """
    ...

def str_to_uuid(value):
    """
    Returns a UUID(value) if the value provided is a str.

    :param value: str or UUID object
    :return: UUID object
    """
    ...

def to_date_field(formatter):
    """
    Returns a callable instance that will convert a string to a Date.

    :param formatter: String that represents data format for parsing.
    :return: instance of the DateConverter.
    """
    class DateConverter(object):
        ...
    
    

def to_datetime_field(formatter):
    """
    Returns a callable instance that will convert a string to a DateTime.

    :param formatter: String that represents data format for parsing.
    :return: instance of the DateTimeConverter.
    """
    class DateTimeConverter(object):
        ...
    
    

def to_time_field(formatter):
    """
    Returns a callable instance that will convert a string to a Time.

    :param formatter: String that represents data format for parsing.
    :return: instance of the TimeConverter.
    """
    class TimeConverter(object):
        ...
    
    

def resolve_class(cls):
    ...

