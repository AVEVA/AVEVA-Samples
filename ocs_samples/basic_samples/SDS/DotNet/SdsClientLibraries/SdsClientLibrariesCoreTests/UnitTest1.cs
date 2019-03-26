using System;
using Xunit;

namespace SdsClientLibrariesCoreTests
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
