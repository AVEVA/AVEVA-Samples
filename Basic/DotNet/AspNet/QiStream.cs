namespace RestSample
{
    public class QiStream
    {
        #region Public Constructors

        public QiStream()
        {
        }

        public QiStream(string name, string typeid)
        {
            Id = name;
            Name = name;
            TypeId = typeid;
        }

        public QiStream(string name, string typeid, string description, string behavior)
        {
            Id = name;
            Name = name;
            TypeId = typeid;
            Description = description;
            BehaviorId = behavior;
        }

        #endregion Public Constructors

        #region Public Properties

        public string BehaviorId { get; set; }
        public string Description { get; set; }
        public string Id { get; set; }

        public string Name { get; set; }
        public string TypeId { get; set; }

        #endregion Public Properties
    }
}