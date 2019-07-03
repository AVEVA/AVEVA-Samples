using IdentityModel.OidcClient.Browser;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace HybridFlow
{
    public class SystemBrowser : IBrowser
    {
        public int Port { get; }
        private readonly string _path;
        public static bool test = false;
        public static string tenant;
        public static string userName;
        public static string password;

        public SystemBrowser(int? port = null, string path = null)
        {
            _path = path;

            if (!port.HasValue)
            {
                Port = GetRandomUnusedPort();
            }
            else
            {
                Port = port.Value;
            }
        }

        private int GetRandomUnusedPort()
        {
            var listener = new TcpListener(IPAddress.Loopback, 0);
            listener.Start();
            var port = ((IPEndPoint) listener.LocalEndpoint).Port;
            listener.Stop();
            return port;
        }

        public async Task<BrowserResult> InvokeAsync(BrowserOptions options)
        {
            using (var listener = new LoopbackHttpListener(Port, _path))
            {
                OpenBrowser(options.StartUrl);

                try
                {
                    var result = await listener.WaitForCallbackAsync();
                    if (String.IsNullOrWhiteSpace(result))
                    {
                        return new BrowserResult
                            {ResultType = BrowserResultType.UnknownError, Error = "Empty response."};
                    }

                    return new BrowserResult {Response = result, ResultType = BrowserResultType.Success};
                }
                catch (TaskCanceledException ex)
                {
                    return new BrowserResult {ResultType = BrowserResultType.Timeout, Error = ex.Message};
                }
                catch (Exception ex)
                {
                    return new BrowserResult {ResultType = BrowserResultType.UnknownError, Error = ex.Message};
                }
            }
        }

        public static void OpenBrowser(string url)
        {
            if (test)
            {
                AutoLogin(url);
                return;
            }

            try
            {
                Process.Start(url);
            }
            catch
            {
                // hack because of this: https://github.com/dotnet/corefx/issues/10361
                if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
                {
                    url = url.Replace("&", "^&");
                    Process.Start(new ProcessStartInfo("cmd", $"/c start {url}") {CreateNoWindow = true});
                }
                else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
                {
                    Process.Start("xdg-open", url);
                }
                else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
                {
                    Process.Start("open", url);
                }
                else
                {
                    throw;
                }
            }
        }


        private static void AutoLogin(string url)
        {
            // Automatic login works against Microsoft personal account option only
            // Must use Live account email that isn't also an AAD account
            // Account must have no 2FA enabled and the login flow must not have any other additional prompts after password entry
            using (IWebDriver driver = new ChromeDriver(Environment.ExpandEnvironmentVariables("%ChromeWebDriver%")))
            {
                driver.Url = url;

                Thread.Sleep(4000);

                driver.FindElement(By.XPath("/html/body/div[3]/div/div/a[@title=\"Personal Account\"]")).Click();


                Thread.Sleep(4000);

                driver.FindElement(By.XPath("//*[@id=\"i0116\"]")).SendKeys(userName);
                driver.FindElement(By.XPath("//*[@id=\"idSIButton9\"]")).Click();


                Thread.Sleep(4000);

                driver.FindElement(By.XPath("//*[@id=\"i0118\"]")).SendKeys(password);
                driver.FindElement(By.XPath("//*[@id=\"idSIButton9\"]")).Click();

                Thread.Sleep(4000);

                driver.Close();
            }
        }
    }



    public class LoopbackHttpListener : IDisposable
    {
        const int DefaultTimeout = 60 * 5; // 5 mins (in seconds)

        IWebHost _host;
        TaskCompletionSource<string> _source = new TaskCompletionSource<string>();
        string _url;

        public string Url => _url;

        public LoopbackHttpListener(int port, string path = null)
        {
            path = path ?? String.Empty;
            if (path.StartsWith("/")) path = path.Substring(1);

            _url = $"https://127.0.0.1:{port}/{path}";

            _host = new WebHostBuilder()
                .UseKestrel()
                .UseUrls(_url)
                .Configure(Configure)
                .Build();
            _host.Start();
        }

        public void Dispose()
        {
            Task.Run(async () =>
            {
                await Task.Delay(500);
                _host.Dispose();
            });
        }

        void Configure(IApplicationBuilder app)
        {
            app.Run(async ctx =>
            {
                if (ctx.Request.Method == "GET")
                {
                    SetResult(ctx.Request.QueryString.Value, ctx);
                }
                else if (ctx.Request.Method == "POST")
                {
                    if (!ctx.Request.ContentType.Equals("application/x-www-form-urlencoded",
                        StringComparison.OrdinalIgnoreCase))
                    {
                        ctx.Response.StatusCode = 415;
                    }
                    else
                    {
                        using (var sr = new StreamReader(ctx.Request.Body, Encoding.UTF8))
                        {
                            var body = await sr.ReadToEndAsync();
                            SetResult(body, ctx);
                        }
                    }
                }
                else
                {
                    ctx.Response.StatusCode = 405;
                }
            });
        }

        private void SetResult(string value, HttpContext ctx)
        {
            try
            {
                ctx.Response.StatusCode = 200;
                ctx.Response.ContentType = "text/html";
                ctx.Response.WriteAsync("<h1>You can now return to the application.</h1>");
                ctx.Response.Body.Flush();

                _source.TrySetResult(value);
            }
            catch
            {
                ctx.Response.StatusCode = 400;
                ctx.Response.ContentType = "text/html";
                ctx.Response.WriteAsync("<h1>Invalid request.</h1>");
                ctx.Response.Body.Flush();
            }
        }

        public Task<string> WaitForCallbackAsync(int timeoutInSeconds = DefaultTimeout)
        {
            Task.Run(async () =>
            {
                await Task.Delay(timeoutInSeconds * 1000);
                _source.TrySetCanceled();
            });

            return _source.Task;
        }
    }
}