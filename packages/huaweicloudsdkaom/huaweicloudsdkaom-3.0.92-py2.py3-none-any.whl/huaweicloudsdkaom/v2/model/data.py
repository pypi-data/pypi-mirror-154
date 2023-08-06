# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class Data:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'result_type': 'str',
        'result': 'list[str]'
    }

    attribute_map = {
        'result_type': 'resultType',
        'result': 'result'
    }

    def __init__(self, result_type=None, result=None):
        """Data

        The model defined in huaweicloud sdk

        :param result_type: 返回值类型。
        :type result_type: str
        :param result: 数据信息。
        :type result: list[str]
        """
        
        

        self._result_type = None
        self._result = None
        self.discriminator = None

        if result_type is not None:
            self.result_type = result_type
        if result is not None:
            self.result = result

    @property
    def result_type(self):
        """Gets the result_type of this Data.

        返回值类型。

        :return: The result_type of this Data.
        :rtype: str
        """
        return self._result_type

    @result_type.setter
    def result_type(self, result_type):
        """Sets the result_type of this Data.

        返回值类型。

        :param result_type: The result_type of this Data.
        :type result_type: str
        """
        self._result_type = result_type

    @property
    def result(self):
        """Gets the result of this Data.

        数据信息。

        :return: The result of this Data.
        :rtype: list[str]
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this Data.

        数据信息。

        :param result: The result of this Data.
        :type result: list[str]
        """
        self._result = result

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Data):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
