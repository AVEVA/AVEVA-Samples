// <copyright file="Program.cs" company="OSIsoft, LLC">
//
// </copyright>


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
using System.Security.Cryptography.X509Certificates;
using System.Net.Security;
using System.Text;

namespace OMF_API
{
    public class Program
    {
        private static readonly HttpClient client = new HttpClient();
        // Set this to zip data going to endpoints
        static bool zip = false;

        // Set this to indicate if the data is going to PI or OCS.  This changes some of the steps taken in the program due to the endpoints accepting different messages.
        static bool sendingToOCS = true;

        // set this to try to force the above bool, otherwise it is determined by what is found in appsettins.json file
        static bool sendingToOCSBoolforced = false;

        static bool VERIFY_SSL = true;




        // The version of the OMFmessages
        static string omfVersion = "1.1";

        // Holders for parameters set by configuration
        static string producerToken;
        static string omfendpoint;
        static string checkBase;
        static string resource;
        static string clientId = "";
        static string clientSecret = "";
        static string pidataserver = "";
        static string piassetserver = "";
        static string afomfdatabase = "";
        static string verify = "";

        static string username = "";
        static string password = "";


        // Holds the token that is used for Auth for OCS.
        static string token = null;

        //Holders for the data message values
        static Random rnd = new Random();
        static bool dynamicBoolHolder = false;
        static int dynamicIntHolder = 0;

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

            //hold on to these in case there is a failure in deleting
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
                //bring in configuration.  Note storing credentials in plain text is not secure or advised
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
                clientId = configuration["clientId"];
                clientSecret = configuration["ClientKey"];
                pidataserver = configuration["dataservername"];
                verify = configuration["VERIFY_SSL"];

                username = configuration["username"];
                password = configuration["password"];
                /* not currently used, but would be needed to check AF creation
                piassetserver = configuration["assetservername"];
                afomfdatabase = configuration["afomfdatabase"];
                */

                if (!sendingToOCSBoolforced)
                {
                    sendingToOCS = tenantId != null;
                }

                // need to make the appropriate url strings for sending and getting values
                if (sendingToOCS)
                {
                    checkBase = $"{resource}/api/{apiVersion}/tenants/{tenantId}/namespaces/{namespaceId}";
                    omfendpoint = checkBase + $"/omf";
                }
                else
                {   
                    checkBase = resource;
                    omfendpoint = checkBase + $"/omf";
                }           

                if(!String.IsNullOrEmpty(verify) && verify == "false")    
                {
                    VERIFY_SSL = false;
                }

                if(!VERIFY_SSL)
                {
                    Console.WriteLine("You are not verifying the certificate of the end point.  This is not advised for any system as there are security issues with doing this.");
                    // this turns off SSL verification
                    //This should not be done in production.  please properly handle your certificates
                    ServicePointManager.ServerCertificateValidationCallback += (sender, cert, chain, sslPolicyErrors) => true;
                }

                // Step 2
                getToken();

                //step 3- 8  are located in here.  
                sendTypesAndContainers();

                int count = 0;
                string value ="";
                while (count == 0  || ((!test) && count < 2))
                {
                    //step 9 
                    var val = create_data_values_for_first_dynamic_type("Container1");
                    value = val;

                    sendValue("data", val);
                    sendValue("data", create_data_values_for_first_dynamic_type("Container2"));
                    sendValue("data", create_data_values_for_second_dynamic_type("Container3"));
                    sendValue("data", create_data_values_for_third_dynamic_type("Container4"));
                    if (sendingToOCS)
                        sendValue("data", create_data_values_for_NonTimeStampIndexAndMultiIndex_type("Container5", "Container6"));
                    Thread.Sleep(1000);
                    count = count + 1;
                }
                CheckValues(value);

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
                try
                {
                    if(sendingToOCS)
                        sendTypesAndContainers("delete");
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.ToString());

                    exc = ex;
                    success = false;
                }

                Console.WriteLine("Done");
                if (!test)
                    Console.ReadLine();
                if (exc != null)
                    throw exc;
            }
            
            return success;
        }

        /// <summary>
        /// Cehcks the last value of Container1 to see if it matches the incoming value
        /// </summary>
        /// <param name="value">last sent value to Container1</param>
        private static void CheckValues(string value)
        {
            Console.WriteLine("Checks");
            Console.WriteLine("Letting OMF get to data store");
            Thread.Sleep(10000);
            
            if (sendingToOCS)
            {
                //give a little bit of time for the OMF information to propogate
                Thread.Sleep(15000);
                // just getting back the type or stream means that it worked
                string json1 = checkValue(checkBase + $"/Types" + $"/FirstDynamicType");

                json1 = checkValue(checkBase + $"/Streams" + $"/Container1");
                json1 = checkValue(checkBase + $"/Streams" + $"/Container1" + $"/Data/last");
                var valueJ = JsonConvert.DeserializeObject<List<JObject>>(value);
                var jsonJ = JsonConvert.DeserializeObject<JObject>(json1);
                if (valueJ[0]["values"][0]["IntegerProperty"]?.ToString() != jsonJ["IntegerProperty"]?.ToString())
                    throw new Exception("Returned value is not expected.");
            }
            else
            {
                string json1 = checkValue(checkBase + $"/dataservers?name=" + pidataserver);
                JObject result = JsonConvert.DeserializeObject<JObject>(json1);
                string pointsURL  = result.Value<JObject>("Links").Value<String>("Points");

                string json2 = checkValue(pointsURL+ "?nameFilter=container1*");
                JObject result2 = JsonConvert.DeserializeObject<JObject>(json2);
                string EndValueUrl = result2.Value<JArray>("Items")[0].Value<JObject>("Links").Value<String>("EndValue");

                string json3 = checkValue(EndValueUrl);

                var valueJ =JsonConvert.DeserializeObject<List<JObject>>(value);
                var jsonJ = JsonConvert.DeserializeObject<JObject>(json3);

                if (valueJ[0]["values"][0]["IntegerProperty"].ToString() != jsonJ["Value"].ToString())
                    throw new Exception("Returned value is not expected.");
            }
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
            if (dynamicIntHolder == 1)
                dynamicIntHolder = 0;
            else
                dynamicIntHolder = 1;
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
                    containerId, getCurrentTime(), dynamicIntHolder.ToString());
        }

        /// <summary>
        /// Wrapper around getting data for the second dynamic type
        /// </summary>
        /// <param name="containerId"></param>
        /// <returns></returns>
        private static string create_data_values_for_second_dynamic_type(string containerId)
        {
            dynamicBoolHolder = !dynamicBoolHolder;
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
                    containerId, getCurrentTime(), rnd.NextDouble()*100, rnd.NextDouble() * 100, dynamicBoolHolder.ToString());
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
                // sendLinks2(action);
                // Step 8
               // sendLinks3(action);
            }
        }

        private static string getBasicAuth()
        {
            String encoded = Convert.ToBase64String(Encoding.GetEncoding("ISO-8859-1").GetBytes(username + ":" + password));
            return ("Basic " + encoded);
        }
        
        /// <summary>
        /// Sends the values to the preconfigured endpoint
        /// </summary>
        /// <param name="messageType"></param>
        /// <param name="dataJson"></param>
        /// <param name="action"></param>
        private static void sendValue(string messageType, string dataJson, string action = "create" )
        {
            WebRequest request = WebRequest.Create(new Uri(omfendpoint));
            request.Method = "post";

            request.Headers.Add("producertoken", producerToken);
            request.Headers.Add("messagetype", messageType);
            request.Headers.Add("action", action);
            request.Headers.Add("messageformat", "json");
            request.Headers.Add("omfversion", omfVersion);

            if (sendingToOCS)
            {
                request.Headers.Add("Authorization", "Bearer " + getToken());
            }
            else
            {
                request.Headers.Add("x-requested-with", "XMLHTTPRequest");
                request.Headers.Add("Authorization", getBasicAuth());
            }


            byte[] byteArray;

            request.ContentType = "application/x-www-form-urlencoded";
            if (!zip)
            {
                byteArray = Encoding.UTF8.GetBytes(dataJson);
            }
            else
            {
                //throw new NotImplementedException();
                
               // byte[] bytes = null;

                using (var msi = new MemoryStream(System.Text.Encoding.UTF8.GetBytes(dataJson)))
                using (var mso = new MemoryStream())
                {
                    using (var gs = new GZipStream(mso, CompressionMode.Compress))
                    {
                        CopyTo(msi, gs);
                    }

                    byteArray = mso.ToArray();
                }
                request.Headers.Add("compression", "gzip");
            }
            request.ContentLength = byteArray.Length;

            Stream dataStream = request.GetRequestStream();
            // Write the data to the request stream.  
            dataStream.Write(byteArray, 0, byteArray.Length);
            // Close the Stream object.  
            dataStream.Close();          

            
            Send(request);
        }
        

        private static string checkValue(string URL)
        {
            WebRequest request = WebRequest.Create(new Uri(URL));
            request.Method = "get";

            if (sendingToOCS)
            {
                request.Headers.Add("Authorization", "Bearer " + getToken());
            }

            else
            {
                request.Headers.Add("x-requested-with", "XMLHTTPRequest");
                request.Headers.Add("Authorization", getBasicAuth());
            }

            return Send(request);
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
        private static string Send(WebRequest request)
        {
            // ServicePointManager.SecurityProtocol = SecurityProtocolType.;s
            using (var resp = request.GetResponse())
            {
                using (HttpWebResponse response = (HttpWebResponse)resp)
                {

                    var stream = resp.GetResponseStream();
                    var code = (int)response.StatusCode;

                    using (StreamReader reader = new StreamReader(stream))
                    { 
                        // Read the content.  
                        string responseString = reader.ReadToEnd();
                        // Display the content.  

                        return responseString;
                    }
                }
            }
        }


        /// <summary>
        /// Wrapper around definition of first static type
        /// </summary>
        /// <param name="action"></param>
        public static void sendFirstStaticType(string action = "create") {
            sendValue("type",
            @"[{
                ""id"": ""FirstStaticTypev2"",
                ""name"": ""First static type"",
                ""classification"": ""static"",
                ""type"": ""object"",
                ""description"": ""First static asset type"",
                ""properties"": {
                    ""index"": {
                        ""type"": ""string"",
                        ""isindex"": true,
                        ""name"": ""name1"",
                        ""description"": ""not in use""
                    },
                    ""name"": {
                        ""type"": ""string"",
                        ""isname"": true,
                        ""name"": ""name2"",
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
                        ""name"": ""name1"",
                        ""description"": ""not in use""
                    },
                    ""name"": {
                        ""type"": ""string"",
                        ""isname"": true,
                        ""name"": ""name2"",
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
                        ""name"": ""name"",
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
                        ""name"": ""name"",
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
                        ""name"": ""name"",
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
                ""typeid"": ""FirstStaticTypev2"",
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
                                ""typeid"": ""FirstStaticTypev2"",
                                ""index"": ""_ROOT""
                        },
                        ""target"": {
                                ""typeid"": ""FirstStaticTypev2"",
                                ""index"": ""Asset1""
                        }
                    },
                    {
                        ""source"": {
                                ""typeid"": ""FirstStaticTypev2"",
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
                            ""typeid"": ""FirstStaticTypev2"",
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
        /// Gets the token for auth for connecting
        /// </summary>
        public static string getToken()
        {
            // PI currently requires no auth
            if (!sendingToOCS)
                return token;

            //use cached version
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

        /// <summary>
        /// Send message using HttpRequestMessage
        /// </summary>
        /// <param name="request"></param>
        /// <returns>The result of the async task of the responding value from the endpoint</returns>
        private static async Task<string> Send(HttpRequestMessage request)
        {
            var response = await client.SendAsync(request);

            var responseString = await response.Content.ReadAsStringAsync();
            if (!response.IsSuccessStatusCode)
                throw new Exception($"Error sending OMF response code:{response.StatusCode}.  Response {responseString}");
            return responseString;
        }

    }
}
