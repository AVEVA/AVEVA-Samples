# SdsTypeProperty.py
#

from enum import Enum


class SdsTypeProperty(object):
    """
    Sds type property definition
    """

    def __init__(self, id=None, name=None, description=None, isKey=False,
                 sdsType=None, value=None, order=None):
        """

        :param id: required
        :param name: not required
        :param description: not required
        :param isKey: bool   Set whether this property is part of the type's
                     index    required
        :param sdsType: SdsType required
        :param value:  object   not required
        :param order: Integer   Determines the order of a complex index type.
                    If isKey is set and this is part of a complex index
                    this is required.   Not required
        """
        self.Id = id
        self.Description = description
        self.IsKey = isKey
        self.SdsType = sdsType
        self.Value = value
        self.Order = order

    @property
    def Id(self):
        """
        required
        :param self:
        :return:
        """
        return self.__id

    @Id.setter
    def Id(self, id):
        """
        required
        :param self:
        :param id:
        :return:
        """
        self.__id = id

    @property
    def Name(self):
        """
        not required
        :param self:
        :return:
        """
        return self.__name

    @Name.setter
    def Name(self, name):
        """
        not required
        :param self:
        :param name:
        :return:
        """
        self.__name = name

    @property
    def Description(self):
        """
        not required
        :param self:
        :return:
        """
        return self.__description

    @Description.setter
    def Description(self, Description):
        """
        not required
        :param self:
        :param Description:
        :return:
        """
        self.__description = Description

    @property
    def IsKey(self):
        """
        bool  Set whether this property is part of the type's index    required
        :param self:
        :return:
        """
        return self.__isKey

    @IsKey.setter
    def IsKey(self, iskey):
        """
        bool  Set whether this property is part of the type's index   required
        :param self:
        :param iskey:
        :return:
        """
        self.__isKey = iskey

    @property
    def SdsType(self):
        """
        required
        :param self:
        :return:
        """
        return self.__sdsType

    @SdsType.setter
    def SdsType(self, sdsType):
        """
        required
        :param self:
        :param sdsType:
        :return:
        """
        self.__sdsType = sdsType

    @property
    def Value(self):
        """
        not required
        :param self:
        :return:
        """
        return self.__value

    @Value.setter
    def Value(self, value):
        """
        not required
        :param self:
        :param value:
        :return:
        """
        self.__value = value

    @property
    def Order(self):
        """
        Integer   Determines the order of a complex index type.
                  If isKey is set and this is part of a complex index
                  this is required.   Not required
        :param self:
        :return:
        """
        return self.__order

    @Order.setter
    def Order(self, order):
        """
        Integer   Determines the order of a complex index type.  If isKey is
                    set and this is part of a complex index  this is required.
                     Not required
        :param self:
        :param order:
        :return:
        """
        self.__order = order

    def toDictionary(self):
        dictionary = {'IsKey': self.IsKey}

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'SdsType'):
            if(self.SdsType):
                from .SdsType import SdsType
                dictionary['SdsType'] = self.SdsType.toDictionary()

        if hasattr(self, 'Value'):
            if (isinstance(self.Value, Enum)):
                dictionary['Value'] = self.Value.name
            else:
                dictionary['Value'] = self.Value

        if hasattr(self, 'Order'):
            dictionary['Order'] = self.Order

        return dictionary

    @staticmethod
    def fromDictionary(content):
        typeProperty = SdsTypeProperty()

        if len(content) == 0:
            return typeProperty

        if 'Id' in content:
            typeProperty.Id = content['Id']

        if 'IsKey' in content:
            typeProperty.IsKey = content['IsKey']

        if 'Name' in content:
            typeProperty.Name = content['Name']

        if 'Description' in content:
            typeProperty.Description = content['Description']

        if 'SdsType' in content:
            from .SdsType import SdsType
            typeProperty.SdsType = SdsType.fromDictionary(content['SdsType'])

        if 'Value' in content:
            typeProperty.Value = content['Value']

        if 'Order' in content:
            typeProperty.Order = content['Order']

        return typeProperty
