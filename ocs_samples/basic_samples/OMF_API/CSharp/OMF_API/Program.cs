
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading;
using System.Net;
using System.IO.Compression;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace OMF_API
{
    public class Program
    {
        private static readonly HttpClient client = new HttpClient();

        // Set this to zip data going to endpoints
        static bool zip = false;

        // Set this to indicate if the data is going to PI or OCS.  This changes some of the steps taken in the program due to the endpoints accepting different messages.
        static bool sendingToOCS = true;

        // The version of the OMFmessages
        static string omfVersion = "1.0";

        // Holders for parameters set by configuration
        static string producerToken;
        static string omfendpoint;
        static string resource;
        static string clientId = "";
        static string clientSecret = "";

        // Holds the token that is used for Auth for OCS.
        static string token = null;

        //Holders for the data message values
        static Random rnd = new Random();
        static bool dynamic2 = false;
        static int dynamic3 = 0;

        static int integer_index1 = 0;
        static int integer_index2_1 = 0;
        static int integer_index2_2 = 0;



        static void Main(string[] args)
        {
            runMain();
        }
        
        /// <summary>
        /// Main function to allow for easy test.
        /// </summary>
        /// <param name="test">Whether this is a test or not</param>
        /// <returns></returns>
        public static bool runMain(bool test= false)
        {
            var success = true;
            Exception exc = null;

            Console.WriteLine(" .d88888b.  888b     d888 8888888888               d8888 8888888b. 8888888 ");
            Console.WriteLine("d88P\" \"Y88b 8888b   d8888 888                     d88888 888   Y88b  888   ");
            Console.WriteLine("888     888 88888b.d88888 888                    d88P888 888    888  888   ");
            Console.WriteLine("888     888 888Y88888P888 8888888               d88P 888 888   d88P  888   ");
            Console.WriteLine("888     888 888 Y888P 888 888                  d88P  888 8888888P\"   888   ");
            Console.WriteLine("888     888 888  Y8P  888 888                 d88P   888 888         888   ");
            Console.WriteLine("Y88b. .d88P 888   \"   888 888                d8888888888 888         888   ");
            Console.WriteLine(" \"Y88888P\"  888       888 888      88888888 d88P     888 888       8888888 ");

            try
            {
                IConfigurationBuilder builder = new ConfigurationBuilder()
                 .SetBasePath(Directory.GetCurrentDirectory())
                 .AddJsonFile("appsettings.json")
                 .AddJsonFile("appsettings.test.json", optional: true);
                IConfiguration configuration = builder.Build();

                // Step 1
                string tenantId = configuration["TenantId"];
                string namespaceId = configuration["NamespaceId"];
                string apiVersion = configuration["ApiVersion"];
                resource = configuration["Resource"];
                producerToken = configuration["ProducerToken"];
                omfendpoint = configuration["omfendpoint"];
                clientId = configuration["clientId"];
                clientSecret = configuration["ClientKey"];

                if (sendingToOCS)
                {
                    omfendpoint = $"{resource}/api/{apiVersion}/tenants/{tenantId}/namespaces/{namespaceId}/omf";
                }
                if (!sendingToOCS)
                    omfVersion = "1.1";

                // Step 2
                getToken();

                //step 3- 8  are located in here.  
                sendTypesAndContainers();

                int count = 0;
                while (count == 0  || ((!test) && count < 2))
                {
                    //step 9 
                    sendValue("data", create_data_values_for_first_dynamic_type("Container1"));
                    sendValue("data", create_data_values_for_first_dynamic_type("Container2"));
                    sendValue("data", create_data_values_for_second_dynamic_type("Container3"));
                    sendValue("data", create_data_values_for_third_dynamic_type("Container4"));
                    if (sendingToOCS)
                        sendValue("data", create_data_values_for_NonTimeStampIndexAndMultiIndex_type("Container5", "Container6"));
                    Thread.Sleep(1000);
                    count = count + 1;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());

                exc = ex;
                success = false;
            }
            finally
            {
                Console.WriteLine("Deleting");
                //step 10
                sendTypesAndContainers("delete");

                Console.WriteLine("Done");
                if (!test)
                    Console.ReadLine();
            }

            if (exc != null)
                throw exc;
            return success;
        }

        /// <summary>
        /// Wrapper around getting data for nontime stamped and multi-index types
        /// </summary>
        /// <param name="NonTimeStampIndexID"></param>
        /// <param name="MultiIndexId"></param>
        /// <returns></returns>
        private static string create_data_values_for_NonTimeStampIndexAndMultiIndex_type(string NonTimeStampIndexID, string MultiIndexId)
        {
            integer_index1 = integer_index1 + 2;

            if (integer_index2_2 % 3 == 0) {
                integer_index2_2 = 1;
                integer_index2_1 = integer_index2_1 + 1;
            }
            else
                integer_index2_2 = integer_index2_2 + 1;

            return String.Format(@"[{{
                        ""containerid"": ""{0}"",
                        ""values"": [
                            {{
                                ""Value"": {1},
                                ""Int_Key"": {2}
                            }},
                            {{
                                ""Value"": {3},
                                ""Int_Key"": {4}
                            }}
                        ]
                    }},
                    {{
                        ""containerid"": ""{5}"",
                        ""values"": [
                            {{
                                ""Value1"":{6},
                                ""Value2"": {7},
                                ""IntKey"": {8},
                                ""IntKey2"": {9}
                            }}
                        ]
                    }}]", NonTimeStampIndexID, rnd.NextDouble()*88, integer_index1, rnd.NextDouble() * 88, integer_index1 +1, MultiIndexId, rnd.NextDouble() * -125, rnd.NextDouble() * 42, integer_index2_1, integer_index2_2);
        }

        /// <summary>
        /// Wrapper around getting data for the third dynamic type
        /// </summary>
        /// <param name="containerId"></param>
        /// <returns></returns>
        private static string create_data_values_for_third_dynamic_type(string containerId)
        {
            if (dynamic3 == 1)
                dynamic3 = 0;
            else
                dynamic3 = 1;
            return String.Format(@"
                    [{{
                        ""containerid"": ""{0}"",
                        ""values"": [
                            {{
                                ""timestamp"": ""{1}"",
                                ""IntegerEnum"": {2}
                            }}
                        ]
                    }}]",
                    containerId, getCurrentTime(), dynamic3.ToString());
        }

        /// <summary>
        /// Wrapper around getting data for the second dynamic type
        /// </summary>
        /// <param name="containerId"></param>
        /// <returns></returns>
        private static string create_data_values_for_second_dynamic_type(string containerId)
        {
            dynamic2 = !dynamic2;
            return String.Format(@"
                    [{{
                        ""containerid"": ""{0}"",
                        ""values"": [
                            {{
                                ""timestamp"": ""{1}"",
                                ""NumberProperty1"": {2},
                                ""NumberProperty2"": {3},
                                ""StringEnum"": ""{4}""
                            }}
                        ]
                    }}]",
                    containerId, getCurrentTime(), rnd.NextDouble()*100, rnd.NextDouble() * 100, dynamic2.ToString());
        }

        /// <summary>
        /// Wrapper around getting data for the first dynamic type
        /// </summary>
        /// <param name="containerId"></param>
        /// <returns></returns>
        private static string create_data_values_for_first_dynamic_type(string containerId)
        {
            return String.Format(@"
                    [{{
                            ""containerid"": ""{0}"",
                        ""values"": [
                            {{
                                ""timestamp"": ""{1}"",
                                ""IntegerProperty"": {2}
                            }}
                        ]
                    }}]", 
                    containerId, getCurrentTime(), rnd.Next(0,100));
        }

        /// <summary>
        /// Gets the current time
        /// </summary>
        /// <returns></returns>
        private static string getCurrentTime()
        {
            return DateTime.Now.ToString("o");
        }

        /// <summary>
        /// Wrapper around the type and container calls
        /// </summary>
        /// <param name="action"></param>
        private static void sendTypesAndContainers(string action = "create")
        {

            // Step 3
            if (!sendingToOCS)
            {
                sendFirstStaticType(action);
                sendSecondStaticType(action);
            }

            // Step 4
            sendFirstDynamicType(action);
            sendSecondDynamicType(action);
            sendThirdDynamicType(action);

            // Step 5
            if (sendingToOCS)
                sendNonTimeStampTypes(action);

            // Step 6
            sendContainers(action);

            if (sendingToOCS)
                sendContainers2(action);
            
            if (!sendingToOCS)
            {
                // Step 7
                sendStaticData(action);
                sendLinks2(action);
                // Step 8
                sendLinks3(action);
            }
        }

        /// <summary>
        /// Sends the values to the preconfigured endpoint
        /// </summary>
        /// <param name="messageType"></param>
        /// <param name="dataJson"></param>
        /// <param name="action"></param>
        private static void sendValue(string messageType, string dataJson, string action = "create" )
        {
            HttpMethod methodTouse = HttpMethod.Post;
            // Encoding utf8 = System.Text.Encoding.UTF8;
            HttpRequestMessage request = new HttpRequestMessage();
            if (!zip)
            {

                request = new HttpRequestMessage()
                {
                    Method = methodTouse,
                    Content = new StringContent(dataJson, System.Text.Encoding.UTF8, "application/json")
                };
                request.Headers.Clear();
            }
            else
            {
                byte[] bytes = null;

                using (var msi = new MemoryStream(System.Text.Encoding.UTF8.GetBytes(dataJson)))
                using (var mso = new MemoryStream())
                {
                    using (var gs = new GZipStream(mso, CompressionMode.Compress))
                    {
                        CopyTo(msi, gs);
                    }

                    bytes = mso.ToArray();
                }
                request = new HttpRequestMessage()
                {
                    Method = methodTouse,
                    Content = new ByteArrayContent(bytes)
                };
                request.Headers.Clear();
                request.Headers.Add("compression", "gzip");

            }

            request.RequestUri = new Uri(omfendpoint);

            if(sendingToOCS)
                request.Headers.Add("Authorization", "Bearer " +getToken());


            request.Headers.Add("producertoken", producerToken);
            request.Headers.Add("messagetype", messageType);
            request.Headers.Add("action", action);
            request.Headers.Add("messageformat", "json");
            request.Headers.Add("omfversion", omfVersion);
            
            Send(request).Wait();
        }

        /// <summary>
        /// Assists in zipping the message if needed
        /// </summary>
        /// <param name="src"></param>
        /// <param name="dest"></param>
        private static void CopyTo(Stream src, Stream dest)
        {
            byte[] bytes = new byte[4096];

            int cnt;

            while ((cnt = src.Read(bytes, 0, bytes.Length)) != 0)
            {
                dest.Write(bytes, 0, cnt);
            }
        }

        /// <summary>
        /// Actual async call to send message to omf endpoint
        /// </summary>
        /// <param name="request"></param>
        /// <returns></returns>
        private static async Task<string> Send(HttpRequestMessage request)
        {
            ServicePointManager.ServerCertificateValidationCallback += (sender, cert, chain, sslPolicyErrors) => true;
            var response = await client.SendAsync(request);

            var responseString = await response.Content.ReadAsStringAsync();
            if (!response.IsSuccessStatusCode)
                throw new Exception($"Error sending OMF response code:{response.StatusCode}.  Response {responseString}");
            return responseString;
        }

        /// <summary>
        /// Wrapper around definition of first static type
        /// </summary>
        /// <param name="action"></param>
        public static void sendFirstStaticType(string action = "create") {
            sendValue("type",
            @"[{
                ""id"": ""FirstStaticType"",
                ""name"": ""First static type"",
                ""classification"": ""static"",
                ""type"": ""object"",
                ""description"": ""First static asset type"",
                ""properties"": {
                    ""index"": {
                        ""type"": ""string"",
                        ""isindex"": true,
                        ""name"": ""not in use"",
                        ""description"": ""not in use""
                    },
                    ""name"": {
                        ""type"": ""string"",
                        ""isname"": true,
                        ""name"": ""not in use"",
                        ""description"": ""not in use""
                    },
                    ""StringProperty"": {
                        ""type"": ""string"",
                        ""name"": ""First configuration attribute"",
                        ""description"": ""First static asset type's configuration attribute""
                    }
                }
            }]", action);
        }

        /// <summary>
        /// wrapper around defintiion of second static type
        /// </summary>
        /// <param name="action"></param>
        public static void sendSecondStaticType(string action = "create")
        {
            sendValue("type",
            @"[{
                ""id"": ""SecondStaticType"",
                ""name"": ""Second static type"",
                ""classification"": ""static"",
                ""type"": ""object"",
                ""description"": ""Second static asset type"",
                ""properties"": {
                    ""index"": {
                        ""type"": ""string"",
                        ""isindex"": true,
                        ""name"": ""not in use"",
                        ""description"": ""not in use""
                    },
                    ""name"": {
                        ""type"": ""string"",
                        ""isname"": true,
                        ""name"": ""not in use"",
                        ""description"": ""not in use""
                    },
                    ""StringProperty"": {
                        ""type"": ""string"",
                        ""name"": ""Second configuration attribute"",
                        ""description"": ""Second static asset type's configuration attribute""
                    }
                }
            }]", action);
            }

        /// <summary>
        /// wrapper around defintiion of first dynamic type
        /// </summary>
        /// <param name="action"></param>
        public static void sendFirstDynamicType(string action = "create") {
            sendValue("type",
            @"[{
               ""id"": ""FirstDynamicType"",
                ""name"": ""First dynamic type"",
                ""classification"": ""dynamic"",
                ""type"": ""object"",
                ""description"": ""not in use"",
                ""properties"": {
                    ""timestamp"": {
                        ""format"": ""date-time"",
                        ""type"": ""string"",
                        ""isindex"": true,
                        ""name"": ""not in use"",
                        ""description"": ""not in use""
                    },
                    ""IntegerProperty"": {
                        ""type"": ""integer"",
                        ""name"": ""Integer attribute"",
                        ""description"": ""PI point data referenced integer attribute""
                    }
                }
            }]", action);
            }

        /// <summary>
        /// wrapper around defintiion of second dynamic type
        /// </summary>
        /// <param name="action"></param>
        public static void sendSecondDynamicType(string action = "create") {
            sendValue("type",
            @"[{
               ""id"": ""SecondDynamicType"",
                ""name"": ""Second dynamic type"",
                ""classification"": ""dynamic"",
                ""type"": ""object"",
                ""description"": ""not in use"",
                ""properties"": {
                    ""timestamp"": {
                        ""format"": ""date-time"",
                        ""type"": ""string"",
                        ""isindex"": true,
                        ""name"": ""not in use"",
                        ""description"": ""not in use""
                    },
                    ""NumberProperty1"": {
                        ""type"": ""number"",
                        ""name"": ""Number attribute 1"",
                        ""description"": ""PI point data referenced number attribute 1"",
                        ""format"": ""float64""
                    },
                    ""NumberProperty2"": {
                        ""type"": ""number"",
                        ""name"": ""Number attribute 2"",
                        ""description"": ""PI point data referenced number attribute 2"",
                        ""format"": ""float64""
                    },
                    ""StringEnum"": {
                        ""type"": ""string"",
                        ""enum"": [""False"", ""True""],
                        ""name"": ""String enumeration"",
                        ""description"": ""String enumeration to replace boolean type""
                    }
                }
            }]", action);
        }

        /// <summary>
        /// wrapper around defintiion of third dynamic type
        /// </summary>
        /// <param name="action"></param>
        public static void sendThirdDynamicType(string action = "create") {
            sendValue("type",
            @"[{
               ""id"": ""ThirdDynamicType"",
                ""name"": ""Third dynamic type"",
                ""classification"": ""dynamic"",
                ""type"": ""object"",
                ""description"": ""not in use"",
                ""properties"": {
                    ""timestamp"": {
                        ""format"": ""date-time"",
                        ""type"": ""string"",
                        ""isindex"": true,
                        ""name"": ""not in use"",
                        ""description"": ""not in use""
                    },
                    ""IntegerEnum"": {
                        ""type"": ""integer"",
                        ""format"": ""int16"",
                        ""name"": ""Integer enumeration"",
                        ""enum"": [0, 1],
                        ""description"": ""Integer enumeration to replace boolean type""
                    }
                }
            }]", action);
        }

        /// <summary>
        /// wrapper around defintiion of non time stamp indexed type and multiindex type
        /// </summary>
        /// <param name="action"></param>
        public static void sendNonTimeStampTypes(string action = "create")
        {
            sendValue("type",
            @"[{
            ""id"": ""NonTimeStampIndex"",
            ""name"": ""NonTimeStampIndex"",
            ""classification"": ""dynamic"",
            ""type"": ""object"",
            ""description"": ""Integer Fun"",
            ""properties"": {
                ""Value"": {
                    ""type"": ""number"",
                    ""name"": ""Value"",
                    ""description"": ""This could be any value""
                },
                ""Int_Key"": {
                    ""type"": ""integer"",
                    ""name"": ""Integer Key"",
                    ""isindex"": True,
                    ""description"": ""A non-time stamp key""
                }
            }
        },        
        {
            ""id"": ""MultiIndex"",
            ""name"": ""Multi_index"",
            ""classification"": ""dynamic"",
            ""type"": ""object"",
            ""description"": ""This one has multiple indicies"",
            ""properties"": {
                ""Value"": {
                    ""type"": ""number"",
                    ""name"": ""Value1"",
                    ""description"": ""This could be any value""
                },                
                ""Value2"": {
                    ""type"": ""number"",
                    ""name"": ""Value2"",
                    ""description"": ""This could be any value too""
                },
                ""IntKey"": {
                    ""type"": ""integer key part 1"",
                    ""name"": ""integer key part 1"",
                    ""isindex"": True,
                    ""description"": ""This could represent any integer value""
                },
                ""IntKey2"": {
                    ""type"": ""integer key part 2"",
                    ""name"": ""integer key part 2"",
                    ""isindex"": True,
                    ""description"": ""This could represent any integer value as well""
                }
            }
        }]", action);
        }

        /// <summary>
        /// wrapper around defintiion of containers
        /// </summary>
        /// <param name="action"></param>
        public static void sendContainers(string action = "create")
        {
            sendValue("container",
            @"[{
                ""id"": ""Container1"",
                ""typeid"": ""FirstDynamicType""
            },
            {
                ""id"": ""Container2"",
                ""typeid"": ""FirstDynamicType""
            },
            {
                ""id"": ""Container3"",
                ""typeid"": ""SecondDynamicType""
            },
            {
                ""id"": ""Container4"",
                ""typeid"": ""ThirdDynamicType""
            }]", action);
        }

        /// <summary>
        /// wrapper around defintiion of containers of non time stamp indexed types
        /// </summary>
        /// <param name="action"></param>
        public static void sendContainers2(string action = "create")
        {
            sendValue("container",
            @"[
            {
            ""id"": ""Container5"",
            ""typeid"": ""NonTimeStampIndex""
            },
            {
                ""id"": ""Container6"",
                ""typeid"": ""MultiIndex""
            }]", action);
        }

        /// <summary>
        /// wrapper around defintiion of data for static types
        /// </summary>
        /// <param name="action"></param>
        public static void sendStaticData(string action = "create")
        {
            sendValue("data",
            @"[{
                ""typeid"": ""FirstStaticType"",
                ""values"": [
                    {
                        ""index"": ""Asset1"",
                        ""name"": ""Parent element"",
                        ""StringProperty"": ""Parent element attribute value""
                    }
                ]
            },
            {
                ""typeid"": ""SecondStaticType"",
                ""values"": [
                    {
                        ""index"": ""Asset2"",
                        ""name"": ""Child element"",
                        ""StringProperty"": ""Child element attribute value""
                    }
                ]
            }]", action);
        }

        /// <summary>
        /// wrapper around defintiion of data for links
        /// </summary>
        /// <param name="action"></param>
        public static void sendLinks2(string action = "create")
        {
            sendValue("data",
            @"[{
                ""typeid"": ""__Link"",
                ""values"": [
                    {
                        ""source"": {
                                ""typeid"": ""FirstStaticType"",
                                ""index"": ""_ROOT""
                        },
                        ""target"": {
                                ""typeid"": ""FirstStaticType"",
                                ""index"": ""Asset1""
                        }
                    },
                    {
                        ""source"": {
                                ""typeid"": ""FirstStaticType"",
                                ""index"": ""Asset1""
                        },
                        ""target"": {
                                ""typeid"": ""SecondStaticType"",
                                ""index"": ""Asset2""
                        }
                    }
                ]
            }    ]", action);
        }


        /// <summary>
        /// wrapper around defintiion of data for links
        /// </summary>
        /// <param name="action"></param>
        public static void sendLinks3(string action = "create")
        {
            sendValue("container",
            @"[{
            ""typeid"": ""__Link"",
            ""values"": [{
                    ""source"": {
                            ""typeid"": ""FirstStaticType"",
                            ""index"": ""Asset1""
                    },
                    ""target"": {
                            ""containerid"": ""Container1""
                    }
                },
                {
                    ""source"": {
                            ""typeid"": ""SecondStaticType"",
                            ""index"": ""Asset2""
                    },
                    ""target"": {
                            ""containerid"": ""Container2""
                    }
                },
                {
                    ""source"": {
                            ""typeid"": ""SecondStaticType"",
                            ""index"": ""Asset2""
                    },
                    ""target"": {
                            ""containerid"": ""Container3""
                    }
                },
                {
                    ""source"": {
                            ""typeid"": ""SecondStaticType"",
                            ""index"": ""Asset2""
                    },
                    ""target"": {
                            ""containerid"": ""Container4""
                    }
                }]", action);
        }


        /// <summary>
        /// Gets the token for auth for connecting to OCS
        /// </summary>
        /// <param name="action"></param>
        public static string getToken()
        {
            if (!String.IsNullOrWhiteSpace(token))
                return token;

            HttpRequestMessage request = new HttpRequestMessage()
                {
                    Method = HttpMethod.Get,
                    RequestUri = new Uri(resource + "/identity/.well-known/openid-configuration")
            };
            request.Headers.Add("Accept", "application/json");

            string res = Send(request).Result;
            var objectContainingURLForAuth = JsonConvert.DeserializeObject<JObject>(res);

            var data = new Dictionary<string, string>
            {
               { "client_id", clientId },
               { "client_secret", clientSecret },
               { "grant_type", "client_credentials" }
            };

            HttpRequestMessage request2 = new HttpRequestMessage()
            {
                Method = HttpMethod.Post,
                RequestUri = new Uri(objectContainingURLForAuth["token_endpoint"].ToString()),
                Content = new FormUrlEncodedContent(data)
            };
            request2.Headers.Add("Accept", "application/json");


            string res2 = Send(request2).Result;

            var tokenObject = JsonConvert.DeserializeObject<JObject>(res2);
            token = tokenObject["access_token"].ToString();
            return token;
        }
    }
}
