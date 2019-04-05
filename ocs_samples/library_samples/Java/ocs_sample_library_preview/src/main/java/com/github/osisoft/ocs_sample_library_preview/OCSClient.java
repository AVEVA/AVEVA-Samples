/** BaseClient.java
 * 
 *  Copyright 2019 OSIsoft, LLC
 *  
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0>
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package  com.github.osisoft.ocs_sample_library_preview;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import  com.github.osisoft.ocs_sample_library_preview.*;
import  com.github.osisoft.ocs_sample_library_preview.sds.*;
import  com.github.osisoft.ocs_sample_library_preview.dataviews.*;

public class OCSClient {
   
    private BaseClient baseClient;
    public DataviewClient Dataviews;  
    public StreamsClient Streams;  
    public TypesClient Types;  
    public Gson mGson = null;

    public OCSClient()
    {
        baseClient = new BaseClient();
        init();
    }

    
    public OCSClient(String apiVersion, String clientId, String clientSecret, String resource)
    {
        baseClient = new BaseClient(apiVersion, clientId, clientSecret, resource);
        init();
    }

    private void init()
    {
        Dataviews = new DataviewClient(baseClient);
        Types = new TypesClient(baseClient);
        Streams = new StreamsClient(baseClient);
        mGson = baseClient.mGson;
    }

    public Map<String,Object>[] jsonStringToMapArray(String input)
    {        
        return mGson.fromJson(input, new TypeToken<Map<String,Object>[]>(){}.getType());
    }

}
