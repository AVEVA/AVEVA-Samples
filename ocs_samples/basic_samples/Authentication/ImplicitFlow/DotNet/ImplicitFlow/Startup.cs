using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;

namespace ImplicitFlow
{
    public class Startup
    {
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            app.UseDefaultFiles();
            app.UseStaticFiles();
        }
    }
}
