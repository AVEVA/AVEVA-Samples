using NUnit.Framework;
using ImplicitFlow;
using System.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System;
using System.IO;
using Microsoft.Extensions.Configuration;


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
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json");
            IConfiguration configuration = builder.Build();

            AutoLogin(configuration["url"], configuration["userName"], configuration["password"]);
        }


        private static void AutoLogin(string url, string userName, string password)
        {
            //  using (IWebDriver driver = new ChromeDriver(Environment.CurrentDirectory))
            using (IWebDriver driver = new ChromeDriver(Environment.ExpandEnvironmentVariables("%ChromeWebDriver%")))
            {
                driver.Url = url;

                Thread.Sleep(4000);
                driver.FindElement(By.XPath("//*[@id=\"login\"]")).Click();

                Thread.Sleep(4000);

                

                driver.FindElement(By.XPath("/html/body/div[3]/div/div/a[2]")).Click();


                Thread.Sleep(4000);

                driver.FindElement(By.XPath("//*[@id=\"i0116\"]")).SendKeys(userName);
                driver.FindElement(By.XPath("//*[@id=\"idSIButton9\"]")).Click();


                Thread.Sleep(4000);

                driver.FindElement(By.XPath("//*[@id=\"i0118\"]")).SendKeys(password);
                driver.FindElement(By.XPath("//*[@id=\"idSIButton9\"]")).Click();

                Thread.Sleep(4000);

                driver.FindElement(By.XPath("//*[@id=\"users\"]")).Click();
                Thread.Sleep(4000);
                
                var results = driver.FindElement(By.XPath("//*[@id=\"users\"]")).Text;

                if (results.Contains("not logged"))
                    throw new Exception("Looging in failed");


                driver.Close();
            }
        }
    }
}