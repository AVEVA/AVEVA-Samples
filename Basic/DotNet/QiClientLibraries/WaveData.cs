using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace QiRestApiCore
{
    public class WaveData
    {
        #region Public Properties

        public double Cos { get; set; }

        public double Cosh { get; set; }

        public int Order { get; set; }

        public double Radians { get; set; }

        public double Sin { get; set; }

        public double Sinh { get; set; }

        public double Tan { get; set; }

        public double Tanh { get; set; }

        public double Tau { get; set; }

        #endregion Public Properties

        #region Public Methods

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.AppendLine($"Order = {Order}");
            builder.AppendLine($"Radians = {Radians}");
            builder.AppendLine($"Tau     = {Tau}");
            builder.AppendLine($"Sine    = {Sin}");
            builder.AppendLine($"Cosine  = {Cos}");
            builder.AppendLine($"Tangent = {Tan}");
            builder.AppendLine($"Sinh    = {Sinh}");
            builder.AppendLine($"Cosh    = {Cosh}");
            builder.AppendLine($"Tanh    = {Tanh}");
            return builder.ToString();
        }

        #endregion Public Methods
    }
}
