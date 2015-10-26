using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RestSample
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
