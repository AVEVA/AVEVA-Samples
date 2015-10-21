namespace RestSample
{
    public class QiTenant
    {
        #region Public Constructors

        public QiTenant(string id)
        {
            Id = id;
        }

        public QiTenant()
        {
            Id = string.Empty;
        }

        #endregion Public Constructors

        #region Public Properties

        public string Id { get; set; }

        #endregion Public Properties
    }
}