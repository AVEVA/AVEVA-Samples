using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
{

    public class QiStreamBehavior
    {
        public string Id
        {
            get;
            set;
        }

        public string Name
        {
            get;
            set;
        }

        public QiStreamMode Mode
        {
            get;
            set;
        }

        public QiStreamExtrapolation ExtrapolationMode
        {
            get;
            set;
        }

        public IList<QiStreamBehaviorOverride> Overrides
        {
            get;
            set;
        }

        public QiStreamBehavior()
        {
            Mode = QiStreamMode.Continuous;
        }
    }
}
