namespace QiRestApiSample
{
    public class QiTenant
    {
        public QiTenant(string id)
        {
            Id = id;
        }

        public QiTenant()
        {
            Id = string.Empty;
        }

        public string Id
        {
            get;
            set;
        }
    }
}
