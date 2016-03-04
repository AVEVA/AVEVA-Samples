namespace QiRestApiSample
{
    public class QiType
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

        public string Description
        {
            get;
            set;
        }

        public QiTypeCode QiTypeCode
        {
            get;
            set;
        }

        public QiTypeProperty[] Properties
        {
            get;
            set;
        }
    }
}
