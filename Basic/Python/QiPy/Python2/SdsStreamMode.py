from enum import Enum

class SdsStreamMode(Enum):
    Continuous = 0
    StepwiseContinuousLeading = 1
    StepwiseContinuousTrailing = 2
    Discrete = 3
    Default = Continuous