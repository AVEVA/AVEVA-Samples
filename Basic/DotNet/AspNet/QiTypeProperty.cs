namespace RestSample
{
    public class QiTypeProperty
    {
        #region Public Properties

        public string Description { get; set; }
        public string Id { get; set; }

        public bool IsKey { get; set; }
        public string Name { get; set; }
        public QiType QiType { get; set; }

        #endregion Public Properties
    }
}