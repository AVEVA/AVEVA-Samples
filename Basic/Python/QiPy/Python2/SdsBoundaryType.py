from enum import Enum

class SdsBoundaryType(Enum):
    Exact = 0
    Inside = 1
    Outside = 2
    ExactOrCalculated = 3
    