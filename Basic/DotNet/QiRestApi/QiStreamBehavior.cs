using System.Collections.Generic;

namespace QiRestApiSample
{
    public class QiStreamBehavior
    {
        public QiStreamBehavior()
        {
            Mode = QiStreamMode.Continuous;
        }

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
    }
}
