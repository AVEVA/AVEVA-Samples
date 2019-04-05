using NUnit.Framework;
using UomsSample;

namespace Tests
{
    public class Tests
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void Test1()
        {
            Assert.True(Program.MainAsync(true).Result);
        }
    }
}