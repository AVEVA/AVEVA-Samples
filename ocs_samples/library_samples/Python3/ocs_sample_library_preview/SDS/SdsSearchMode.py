# SdsSearchMode.py
#

from enum import Enum


class SdsSearchMode(Enum):
    """Search enum 0-4"""
    Exact = 0
    ExactOrNext = 1
    Next = 2
    ExactOrPrevious = 3
    Previous = 4
