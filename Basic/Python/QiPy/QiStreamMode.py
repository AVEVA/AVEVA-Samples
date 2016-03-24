from enum import Enum

class QiStreamMode(Enum):
    Continuous = 0
    StepwiseContinuousLeading = 1
    StepwiseContinuousTrailing = 2
    Discrete = 3
    Default = Continuous