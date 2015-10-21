using System;
using System.Text;

namespace RestSample
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

        public static WaveData Next(TimeSpan interval, double multiplier, int order)
        {
            var now = DateTime.UtcNow;
            var timeOfDay = now.TimeOfDay;

            var radians = ((timeOfDay.TotalMilliseconds % interval.TotalMilliseconds) / interval.TotalMilliseconds) * 2 *
                          Math.PI;

            return new WaveData
            {
                Order = order,
                Radians = radians,
                Tau = radians / (2 * Math.PI),
                Sin = multiplier * Math.Sin(radians),
                Cos = multiplier * Math.Cos(radians),
                Tan = multiplier * Math.Tan(radians),
                Sinh = multiplier * Math.Sinh(radians),
                Cosh = multiplier * Math.Cosh(radians),
                Tanh = multiplier * Math.Tanh(radians)
            };
        }

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