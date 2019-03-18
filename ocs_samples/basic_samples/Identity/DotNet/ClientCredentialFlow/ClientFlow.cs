//ClientFlow.cs
//Copyright 2019 OSIsoft, LLC
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//<http://www.apache.org/licenses/LICENSE-2.0>
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

using System;
using System.Net.Http;
using OSIsoft.Identity;

namespace ClientCredentialFlow
{
    public static class ClientFlow
    {
        private static string _ocsUrl;

        public static string OcsUrl
        {
            set => _ocsUrl = value;
        }

        public static HttpClient AuthenticatedHttpClient { get; private set; }

        public static void CreateAuthenticatedHttpClient(string clientId, string clientSecret)
        {
            Console.WriteLine("+-------------------------------------+");
            Console.WriteLine("|  Sign in with Client Credentials    |");
            Console.WriteLine("+-------------------------------------+");
            Console.WriteLine("");

            AuthenticatedHttpClient = new HttpClient(InitiateAuthenticationHandler(clientId, clientSecret))
            {
                BaseAddress = new Uri(_ocsUrl)
            };
        }

        private static AuthenticationHandler InitiateAuthenticationHandler(string clientId, string clientSecret)
        {
            // Create an instance of the AuthenticationHandler.
            return new AuthenticationHandler(_ocsUrl, clientId, clientSecret)
            {
                InnerHandler = new HttpClientHandler()
                {
                    AllowAutoRedirect = false,
                }
            };
        }
    }
}
