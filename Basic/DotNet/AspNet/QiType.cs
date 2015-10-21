namespace RestSample
{
    public class QiType
    {
        #region Public Properties

        public string Description { get; set; }
        public string Id { get; set; }

        public string Name { get; set; }
        public QiTypeProperty[] Properties { get; set; }
        public QiTypeCode QiTypeCode { get; set; }

        #endregion Public Properties
    }
}