from enum import Enum

class QiStreamMode(Enum):
        Default = Continuous
        Continuous = 0
        StepwiseContinuousLeading = 1
        StepwiseContinuousTrailing = 2
        Discrete = 3