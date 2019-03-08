/** Program.java
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

package com.github.osisoft.omfapi;


//import com.google.gson.reflect.TypeToken;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;


/**
 * Hello world!
 *
 */
public class Program 
{
    
    static String tenantId = getConfiguration("tenantId");
    static String namespaceId = getConfiguration("namespaceId");
	
    public static void main( String[] args )
    {
        toRun(false);
    }        
    
    public static boolean toRun(Boolean test) {
        Boolean success = true;
        // Create Sds client to communicate with server
        System.out.println("------------------------------------------------------------------");
        System.out.println(" .d88888b.  888b     d888 8888888888        8888888b. Y88b   d88P ");
        System.out.println("d88P\" \"Y88b 8888b   d8888 888               888   Y88b Y88b d88P  ");
        System.out.println("888     888 88888b.d88888 888               888    888  Y88o88P   ");
        System.out.println("888     888 888Y88888P888 8888888           888   d88P   Y888P    ");
        System.out.println("888     888 888 Y888P 888 888               8888888P\"     888     ");
        System.out.println("888     888 888  Y8P  888 888               888           888     ");
        System.out.println("Y88b. .d88P 888   \"   888 888               888           888     ");
        System.out.println(" \"Y88888P\"  888       888 888      88888888 888           888     ");
        System.out.println("------------------------------------------------------------------");

        try {
            String resource = getConfiguration("resource");
            String clientId = getConfiguration("clientId");
            String clientSecret = getConfiguration("clientSecret");
            String apiVersion = getConfiguration("apiVersion");
            String omfEndPoint = getConfiguration("completedURL");
            
            if (omfEndPoint.equals("")){
                omfEndPoint = omfEndPoint;
            }
            else{
                omfEndPoint = resource + "/api/" + apiVersion + "/tenants/" + tenantId + "/namespaces/" + namespaceId + "/omf";
            }
            oneTimeSendMessages()

            int count = 0;
            while (!test && count < 10);
                send_omf_message_to_endpoint("data", create_data_values_for_first_dynamic_type("container1"))
                send_omf_message_to_endpoint("data", create_data_values_for_first_dynamic_type("container2"))
                send_omf_message_to_endpoint("data", create_data_values_for_second_dynamic_type("container3"))
                send_omf_message_to_endpoint("data", create_data_values_for_third_dynamic_type("container4"))
                send_omf_message_to_endpoint("data", create_data_values_for_NonTimeStampIndexAndMultiIndex_type("container5", "container6"))
                time.sleep(1)
                count = count +1;
            }
        catch (Exception e) {
            success = false;
            e.printStackTrace();
        } finally {

        }



        return success;
    }
    
    private static String getConfiguration(String propertyId) {
        String property = "";
        Properties props = new Properties();
        InputStream inputStream;

        try {
            System.out.println(new File(".").getAbsolutePath());
            inputStream = new FileInputStream("config.properties");
            props.load(inputStream);
            property = props.getProperty(propertyId);
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return property;
    }
}
