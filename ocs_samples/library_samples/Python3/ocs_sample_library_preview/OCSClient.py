# OCSClient.py
#

from .BaseClient import BaseClient
from .Dataviews import Dataviews
from .Types import Types
from .Streams import Streams


class OCSClient:
    """
    A client that handles communication with OCS
    """

    def __init__(self, apiversion, tenant, url, clientId, clientSecret,
                 acceptVerbosity=False):
        """
        Use this to help comuninaication with OCS
        :param apiversion: Version of the api you are communicating with
        :param tenant: Your tenant ID
        :param url: The base URL for your OCS instance
        :param clientId: Your client ID
        :param clientSecret: Your client Secret or Key
        :param acceptVerbosity: Sets whether in value calls you get all values
                or just non-default values
        """
        self.__baseClient = BaseClient(apiversion, tenant, url, clientId,
                                       clientSecret, acceptVerbosity)
        self.__Dataviews = Dataviews(self.__baseClient)
        self.__Types = Types(self.__baseClient)
        self.__Streams = Streams(self.__baseClient)

    @property
    def uri(self):
        """
        :return: The uri of this OCS client as a string
        """
        return self.__baseClient.uri

    @property
    def tenant(self):
        """
        :return: The tenant of this OCS client as a string
        """
        return self.__baseClient.tenant

    @property
    def acceptverbosity(self):
        """
        :return: Whether this will include the accept verbosity header
        """
        return self.__baseClient.AcceptVerbosity

    @acceptverbosity.setter
    def acceptverbosity(self, AcceptVerbosity):
        self.__baseClient.AcceptVerbosity = AcceptVerbosity

    @property
    def request_timeout(self):
        """
        :return: Request timeout in seconds (default 30 secs)
        """
        return self.__baseClient.RequestTimeout

    @request_timeout.setter
    def request_timeout(self, timeout):
        self.__baseClient.RequestTimeout = timeout

    @property
    def Dataviews(self):
        """
        :return: A client for interacting with Dataviews
        """
        return self.__Dataviews

    @property
    def Types(self):
        """
        :return: A client for interacting with Types
        """
        return self.__Types

    @property
    def Streams(self):
        """
        :return: A client for interacting with Streams
        """
        return self.__Streams
