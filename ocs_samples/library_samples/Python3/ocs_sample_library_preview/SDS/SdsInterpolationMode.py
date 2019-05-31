
# SdsInterpolationMode.py
#

from enum import Enum

class SdsInterpolationMode(Enum):
    """
    SdsInterpolationMode 0 -3
    """
    Continuous = 0	            # The default InterpolationMode is Continuous. 
                                    # Interpolates the data using previous and next index values
    StepwiseContinuousLeading = 1   # Returns the data from the previous index
    StepwiseContinuousTrailing	= 2 # Returns the data from the next index
    Discrete = 3                    # Returns 'null'
