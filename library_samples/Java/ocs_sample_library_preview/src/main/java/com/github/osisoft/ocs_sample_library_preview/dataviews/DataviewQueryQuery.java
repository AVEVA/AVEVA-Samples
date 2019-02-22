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
    private String Operator = "";

    public DataviewQueryQuery()
    {
    }

    public DataviewQueryQuery(String resource, String field, String Value, String Operator)
    {
        this.Resource =resource;
        this.Field =field;
        this.Value = Value;
        this.Operator = Operator;
    }

    public String getResource() {
        return Resource;
    }

    public void setResource(String resource) {
        this.Resource = resource;
    }

    public String getField() {
        return Field;
    }

    public void setField(String field) {
        this.Field = field;
    }

    public String getValue() {
        return Value;
    }

    public void setValue(String value) {
        this.Value = value;
    }

    public String getOperator() {
        return Operator;
    }

    public void setOperator(String operator) {
        this.Operator = operator;
    }
}
