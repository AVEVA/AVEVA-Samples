using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
{
    public class QiStream
    {
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

        public string TypeId
        {
            get;
            set;
        }
        
        public string BehaviorId
        {
            get;
            set;
        }
    }
}
