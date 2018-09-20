<# sds_type_property.py

   Copyright (C) 2018 OSIsoft, LLC. All rights reserved.

   THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
   OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
   THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.

   RESTRICTED RIGHTS LEGEND
   Use, duplication, or disclosure by the Government is subject to restrictions
   as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
   Computer Software clause at DFARS 252.227.7013

   OSIsoft, LLC
   1600 Alvarado St, San Leandro, CA 94577
#>

from enum import Enum
import sds_type


class SdsTypeProperty(object):
    """Sds type property definition"""
    def __init__(self):
        self.__IsKey = False

    @property
    def Id(self):
        return self.__id

    @Id.setter
    def Id(self, id):
        self.__id = id

    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, name):
        self.__name = name

    @property
    def Description(self):
        return self.__description

    @Description.setter
    def Description(self, description):
        self.__description = description

    @property
    def IsKey(self):
        return self.__IsKey

    @IsKey.setter
    def IsKey(self, IsKey):
        self.__IsKey = IsKey

    @property
    def SdsType(self):
        return self.__SdsType

    @SdsType.setter
    def SdsType(self, SdsType):
        self.__SdsType = SdsType

    def to_dictionary(self):
        dictionary = {'IsKey': self.IsKey}

        if hasattr(self, 'Id'):
            dictionary['Id'] = self.Id

        if hasattr(self, 'Name'):
            dictionary['Name'] = self.Name

        if hasattr(self, 'Description'):
            dictionary['Description'] = self.Description

        if hasattr(self, 'SdsType'):
            dictionary['SdsType'] = self.SdsType.to_dictionary()

        if hasattr(self, 'Value'):
            if isinstance(self.Value, Enum):
                dictionary['Value'] = self.Value.name
            else:
                dictionary['Value'] = self.Value

        if hasattr(self, 'Order'):
            dictionary['Order'] = self.Order

        return dictionary

    @staticmethod
    def from_dictionary(content):
        prop_names = ['Id', 'IsKey', 'Name', 'Description', 'SdsType', 'Value', 'Order']
        type_property = SdsTypeProperty()

        if len(content) == 0:
            return type_property

        for prop_name in prop_names:
            if prop_name in content:
                if prop_name == 'SdsType':
                    val = sds_type.SdsType.from_dictionary(content['SdsType'])
                else:
                    val = content[prop_name]
                type_property.__setattr__(prop_name, val)

        return type_property
