/** DataviewQueryQuery.java
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

package  com.github.osisoft.ocs_sample_library_preview.dataviews;


public class DataviewQueryQuery {

    private String Resource = "";
    private String Field = "";
    private String Value = "";
    private String Function = "";

    /**
     * base constructor
     */
    public DataviewQueryQuery()
    {
    }

    /**
     * generate the query from passed in values
     * 
     * @param Resource query resource can be something like "Streams", "TypeProperties"   required
     * @param Field query field can be something like "Id", "Name", "Tag", "Description", "TypeId", "MetadataKey"   required
     * @param Value value for field to use in query   required
     * @param Function  QueryFunction can be something like "Contains", "Equals", "EndsWith", "StartsWith"    required
     */
    public DataviewQueryQuery(String resource, String field, String Value, String Function)
    {
        this.Resource =resource;
        this.Field =field;
        this.Value = Value;
        this.Function = Function;
    }

    /**
     * gets resource   query resource can be something like "Streams", "TypeProperties" 
     * @return
     */
    public String getResource() {
        return Resource;
    }

    /**
     * sets resource    query resource can be something like "Streams", "TypeProperties" 
     * @param resource
     */
    public void setResource(String resource) {
        this.Resource = resource;
    }

    /**
     * gets field   query field can be something like "Id", "Name", "Tag", "Description", "TypeId", "MetadataKey"  
     * @return
     */
    public String getField() {
        return Field;
    }

    /**
     * sets field   query field can be something like "Id", "Name", "Tag", "Description", "TypeId", "MetadataKey"  
     * @param field
     */
    public void setField(String field) {
        this.Field = field;
    }

    /**
     * get value   value for field to use in query 
     * @return
     */
    public String getValue() {
        return Value;
    }

    /**
     * sets value   value for field to use in query 
     * @param value
     */
    public void setValue(String value) {
        this.Value = value;
    }

    /**
     * gets function    QueryFunction can be something like "Contains", "Equals", "EndsWith", "StartsWith"  
     * @return
     */
    public String getFunction() {
        return Function;
    }

    /**
     * sets function    QueryFunction can be something like "Contains", "Equals", "EndsWith", "StartsWith"  
     * @param function
     */
    public void setFunction(String function) {
        this.Function = function;
    }
}
