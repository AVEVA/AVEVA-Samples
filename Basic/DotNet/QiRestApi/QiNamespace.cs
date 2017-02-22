using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace QiRestApiSample
{
    public class QiNamespace
    {
        public QiNamespace()
        {
            this.Id = "Default";
        }

        public QiNamespace(string id)
        {
            this.Id = id;
        }

        public string Id { get; set; }
    }
}
