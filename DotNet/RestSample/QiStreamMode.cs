using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
{
    public enum QiStreamMode
    {
        Default = Continuous,
        Continuous = 0,
        StepwiseContinuousLeading = 1,
        StepwiseContinuousTrailing = 2,
        Discrete = 3,
    }
}
