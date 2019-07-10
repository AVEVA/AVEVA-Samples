/** BaseClient.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.util.Map;

import  com.github.osisoft.ocs_sample_library_preview.sds.*;
import  com.github.osisoft.ocs_sample_library_preview.dataviews.*;

/**
 * Client to call into for interacting with OCS
 */
public class OCSClient {
   
    /**
     * Client to help with interactions with dataviews
     */
    public DataviewClient Dataviews;  
    /**
     * Client to help with interactions with streams
     */
    public StreamsClient Streams;  
    /**
     * Client to help with interactions with types
     */
    public TypesClient Types;  
    /**
     * Helper with json actions
     */
    public Gson mGson = null;

    
    private BaseClient baseClient;

    /**
    *  Client to call into for interacting with OCS.  Is configured from config file running at base program's folder
     */
    public OCSClient()
    {
        baseClient = new BaseClient();
        init();
    }

    /**
    *  Client to call into for interacting with OCS.  Is configured from config file running at base program's folder.  
     * @param apiVersion APIversion of OCS
     * @param clientId Client id to login with
     * @param clientSecret client secret to login with 
     * @param resource OCS url
     */
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

    /**
     * Helper function used in some of the clients
     * @param input json string 
     * @return Map<String,Object>[] 
     */
    public Map<String,Object>[] jsonStringToMapArray(String input)
    {        
        return mGson.fromJson(input, new TypeToken<Map<String,Object>[]>(){}.getType());
    }

}
