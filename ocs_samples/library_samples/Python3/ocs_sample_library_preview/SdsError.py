# SdsError.py
#


class SdsError(Exception):
    """
    Helper class to hold exceptions
    """
    def __init__(self, value):
        """
        Set thee exception value
        :param value:
        """
        self.value = value

    def __str__(self):
        """
        Get the exception
        :return:
        """
        return repr(self.value)
