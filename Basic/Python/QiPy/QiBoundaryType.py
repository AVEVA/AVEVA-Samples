from enum import Enum

class QiBoundaryType(Enum):
    Exact = 0
    Inside = 1
    Outside = 2
    ExactOrCalculated = 3
    