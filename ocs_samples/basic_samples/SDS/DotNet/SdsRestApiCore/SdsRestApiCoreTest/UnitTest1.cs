using System;
using Xunit;

namespace SdsRestApiCoreTest
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            Assert.True(SdsRestApiCore.Program.MainAsync(true).Result);
        }
    }
}
