/** Dataview.java
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


public class Dataview {

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private DataviewQuery[] Queries;
    private DataviewMapping Mappings;
    private DataviewIndexConfig IndexConfig;
    private String IndexDataType = "";

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getDescription() {
        return Description;
    }

    public void setDescription(String description) {
        this.Description = description;
    }

    public DataviewQuery[] getQueries() {
        return Queries;
    }

    public void setQueries(DataviewQuery[] queries) {
        this.Queries = queries;
    }

    public DataviewMapping getMappings() {
        return Mappings;
    }

    public void setMappings(DataviewMapping mappings) {
        this.Mappings = mappings;
    }

    public DataviewIndexConfig getIndexConfig() {
        return IndexConfig;
    }

    public void setQueries(DataviewIndexConfig indexConfig) {
        this.IndexConfig = indexConfig;
    }

    public String getIndexDataType() {
        return IndexDataType;
    }

    public void setIndexDataType(String indexDataType) {
        this.IndexDataType = indexDataType;
    }
}
