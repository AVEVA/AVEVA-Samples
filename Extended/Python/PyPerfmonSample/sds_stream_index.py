import json


class SdsStreamIndex(object):
    """Sds Stream Index definitions"""

    @property
    def sds_type_property_id(self):
        return self.__sds_type_property_id

    @sds_type_property_id.setter
    def sds_type_property_id(self, sds_type_property_id):
        self.__sds_type_property_id = sds_type_property_id

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def to_dictionary(self):
        # required properties
        dictionary = {'sds_type_property_id': self.sds_type_property_id}

        return json.loads(dictionary)

    @staticmethod
    def from_dictionary(content):
        type_property_id = SdsStreamIndex()

        if len(content) == 0:
            return type_property_id

        if 'sds_type_property_id' in content:
            type_property_id.sds_type_property_id = content['sds_type_property_id']

        return type_property_id
