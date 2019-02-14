/** DataviewQuery.java
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


public class DataviewQuery {

    private String Id = "";
    private DataviewQueryQuery Query;

    public DataviewQuery( )
    {
        this.Query = new DataviewQueryQuery();
    }

    public DataviewQuery(String Id, String Type, String Value, String Operator )
    {
        this.Id = Id;
        this.Query = new DataviewQueryQuery(Type, Value, Operator);
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public DataviewQueryQuery getQuery() {
        return Query;
    }

    public void setQuery(DataviewQueryQuery query) {
        this.Query = query;
    }
}
