using System;
using Xunit;

namespace OMF_APITests
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            Assert.True(OMF_API.Program.runMain(true));
        }
    }
}
