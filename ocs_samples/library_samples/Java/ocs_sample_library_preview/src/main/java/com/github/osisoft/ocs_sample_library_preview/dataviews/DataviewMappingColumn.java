/** DataviewMappingColumn.java
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

import java.util.Map;

public class DataviewMappingColumn {

    private String Name = "";
    private String IsKey = "";
    private String DataType = "";
    private DataviewMappingRule MappingRule;

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getIsKey() {
        return IsKey;
    }

    public void setIsKey(String isKey) {
        this.IsKey = isKey;
    }

    public String getDataType() {
        return DataType;
    }

    public void setDataType(String dataType) {
        this.DataType = dataType;
    }

    public DataviewMappingRule  getMappingRule() {
        return MappingRule;
    }

    public void setMappingRule(DataviewMappingRule mappingRule) {
        this.MappingRule = mappingRule;
    }
}
