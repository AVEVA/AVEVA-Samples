
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

namespace OMF_API
{
    public class Program
    {
        private static readonly HttpClient client = new HttpClient();

        static string producerToken;
        static string omfendpoint;
        static bool zip = false;

        static void Main(string[] args)
        {
            runMain();
        }

        public static bool runMain(bool test= false)
        {
            var success = true;
            IConfigurationBuilder builder = new ConfigurationBuilder()
             .SetBasePath(Directory.GetCurrentDirectory())
             .AddJsonFile("appsettings.json")
             .AddJsonFile("appsettings.test.json", optional: true);
            IConfiguration configuration = builder.Build();

            string tenantId = configuration["TenantId"];
            string namespaceId = configuration["NamespaceId"];
            string resource = configuration["Resource"];
            string apiVersion = configuration["ApiVersion"];
            producerToken = configuration["ProducerToken"];
            omfendpoint = configuration["omfendpoint"];

            if (String.IsNullOrWhiteSpace(omfendpoint))
            {
                omfendpoint = $"{resource}/api/{apiVersion}/tenants/{tenantId}/namespaces/{namespaceId}/omf";
            }

            sendTypesAndContainers();

            return success;
        }

        private static void sendTypesAndContainers()
        {
            sendFirstStaticType();
            sendSecondStaticType();
            sendFirstDynamicType();
            sendSecondDynamicType();
            sendThirdDynamicType();
            sendNonTimeStampTypes();
        }

        private static void sendValue(string messageType, string dataJson )
        {
            HttpMethod methodTouse = HttpMethod.Post;
            // Encoding utf8 = System.Text.Encoding.UTF8;
            HttpRequestMessage request = new HttpRequestMessage();
            request.RequestUri = new Uri(omfendpoint);
            request.Headers.Clear();

            if (!zip)
            {

                request = new HttpRequestMessage()
                {
                    Method = methodTouse,
                    Content = new StringContent(dataJson, System.Text.Encoding.UTF8, "application/json")
                };
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
                request.Headers.Add("compression", "gzip");

            }

            request.Headers.Add("producertoken", producerToken);
            request.Headers.Add("messagetype", messageType);
            request.Headers.Add("action", "create");
            request.Headers.Add("messageformat", "json");
            request.Headers.Add("omfversion", "1.0");
            
            Send(request).Wait();
        }


        private static void CopyTo(Stream src, Stream dest)
        {
            byte[] bytes = new byte[4096];

            int cnt;

            while ((cnt = src.Read(bytes, 0, bytes.Length)) != 0)
            {
                dest.Write(bytes, 0, cnt);
            }
        }

        private static async Task Send(HttpRequestMessage request)
        {
            ServicePointManager.ServerCertificateValidationCallback += (sender, cert, chain, sslPolicyErrors) => true;
            var response = await client.SendAsync(request);

            var responseString = await response.Content.ReadAsStringAsync();
            if (!response.IsSuccessStatusCode)
                throw new Exception($"Error sending OMF response code:{response.StatusCode}.  Response {responseString}");
        }

        public static void sendFirstStaticType() {
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
            }]");
        }

        public static void sendSecondStaticType()
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
            }]");
            }

        public static void sendFirstDynamicType() {
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
            }]");
            }

        public static void sendSecondDynamicType() {
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
            }]");
        }

        public static void sendThirdDynamicType() {
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
            }]");
        }

        public static void sendNonTimeStampTypes()
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
        }]");
        }


        public static void sendContainers()
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
            }]");
        }

        public static void sendContainers2()
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
            }]");
        }

        public static void sendLinks1()
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
            }]");
        }

        public static void sendLinks2()
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
            }    ]");
        }

        public static void sendLink3()
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
                }]");
        }


    }
}
