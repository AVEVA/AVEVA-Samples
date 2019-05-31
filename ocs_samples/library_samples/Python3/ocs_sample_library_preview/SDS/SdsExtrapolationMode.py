# SdsStreamExtrapolationMode.py
#

from enum import Enum

class SdsExtrapolationMode(Enum):
    """
    SdsStreamExtrapolationMode 0 -3
    """
    All = 0
    Nonex = 1
    Forward = 2
    Backward = 3


