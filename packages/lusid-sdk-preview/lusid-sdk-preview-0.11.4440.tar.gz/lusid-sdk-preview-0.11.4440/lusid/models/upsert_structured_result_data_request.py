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


class UpsertStructuredResultDataRequest(object):
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
        'id': 'StructuredResultDataId',
        'data': 'StructuredResultData'
    }

    attribute_map = {
        'id': 'id',
        'data': 'data'
    }

    required_map = {
        'id': 'required',
        'data': 'optional'
    }

    def __init__(self, id=None, data=None, local_vars_configuration=None):  # noqa: E501
        """UpsertStructuredResultDataRequest - a model defined in OpenAPI"
        
        :param id:  (required)
        :type id: lusid.StructuredResultDataId
        :param data: 
        :type data: lusid.StructuredResultData

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._data = None
        self.discriminator = None

        self.id = id
        if data is not None:
            self.data = data

    @property
    def id(self):
        """Gets the id of this UpsertStructuredResultDataRequest.  # noqa: E501


        :return: The id of this UpsertStructuredResultDataRequest.  # noqa: E501
        :rtype: lusid.StructuredResultDataId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UpsertStructuredResultDataRequest.


        :param id: The id of this UpsertStructuredResultDataRequest.  # noqa: E501
        :type id: lusid.StructuredResultDataId
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def data(self):
        """Gets the data of this UpsertStructuredResultDataRequest.  # noqa: E501


        :return: The data of this UpsertStructuredResultDataRequest.  # noqa: E501
        :rtype: lusid.StructuredResultData
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this UpsertStructuredResultDataRequest.


        :param data: The data of this UpsertStructuredResultDataRequest.  # noqa: E501
        :type data: lusid.StructuredResultData
        """

        self._data = data

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
        if not isinstance(other, UpsertStructuredResultDataRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpsertStructuredResultDataRequest):
            return True

        return self.to_dict() != other.to_dict()
