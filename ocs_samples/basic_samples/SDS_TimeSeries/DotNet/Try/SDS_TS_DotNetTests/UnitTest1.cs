using System;
using Xunit;

namespace SDS_TS_DotNetTests
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            Assert.True(SdsClientLibraries.Program.MainAsync(true).Result);

        }
    }
}
