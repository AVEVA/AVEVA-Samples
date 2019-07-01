using System;
using Xunit;

namespace SDS_TS_DotNetTests
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            Assert.True(SDS_TS_DotNet.Program.MainAsync(true).Result);
        }
    }
}
