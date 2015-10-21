using System.Collections.Generic;

namespace RestSample
{
    public class QiStreamBehavior
    {
        #region Public Constructors

        public QiStreamBehavior()
        {
            Mode = QiStreamMode.Continuous;
        }

        #endregion Public Constructors

        #region Public Properties

        public QiStreamExtrapolation ExtrapolationMode { get; set; }
        public string Id { get; set; }

        public QiStreamMode Mode { get; set; }
        public string Name { get; set; }
        public IList<QiStreamBehaviorOverride> Overrides { get; set; }

        #endregion Public Properties
    }
}