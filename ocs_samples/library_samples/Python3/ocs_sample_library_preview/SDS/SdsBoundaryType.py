# SdsBoundaryType.py
#

from enum import Enum


class SdsBoundaryType(Enum):
    """
    Enum for boundary types 0-3
    """
    Exact = 0
    Inside = 1
    Outside = 2
    ExactOrCalculated = 3
