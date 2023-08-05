# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.4440
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class FieldValue(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'value': 'str',
        'fields': 'dict(str, str)'
    }

    attribute_map = {
        'value': 'value',
        'fields': 'fields'
    }

    required_map = {
        'value': 'required',
        'fields': 'required'
    }

    def __init__(self, value=None, fields=None, local_vars_configuration=None):  # noqa: E501
        """FieldValue - a model defined in OpenAPI"
        
        :param value:  (required)
        :type value: str
        :param fields:  (required)
        :type fields: dict(str, str)

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._value = None
        self._fields = None
        self.discriminator = None

        self.value = value
        self.fields = fields

    @property
    def value(self):
        """Gets the value of this FieldValue.  # noqa: E501


        :return: The value of this FieldValue.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this FieldValue.


        :param value: The value of this FieldValue.  # noqa: E501
        :type value: str
        """
        if self.local_vars_configuration.client_side_validation and value is None:  # noqa: E501
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and len(value) > 512):
            raise ValueError("Invalid value for `value`, length must be less than or equal to `512`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and len(value) < 1):
            raise ValueError("Invalid value for `value`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                value is not None and not re.search(r'^[\s\S]*$', value)):  # noqa: E501
            raise ValueError(r"Invalid value for `value`, must be a follow pattern or equal to `/^[\s\S]*$/`")  # noqa: E501

        self._value = value

    @property
    def fields(self):
        """Gets the fields of this FieldValue.  # noqa: E501


        :return: The fields of this FieldValue.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._fields

    @fields.setter
    def fields(self, fields):
        """Sets the fields of this FieldValue.


        :param fields: The fields of this FieldValue.  # noqa: E501
        :type fields: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and fields is None:  # noqa: E501
            raise ValueError("Invalid value for `fields`, must not be `None`")  # noqa: E501

        self._fields = fields

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FieldValue):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FieldValue):
            return True

        return self.to_dict() != other.to_dict()
