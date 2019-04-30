/** DataviewMapping.java
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

/**
 * DataviewMapping
 */
public class DataviewMapping {

    private Boolean IsDefault = true;
    private DataviewMappingColumn[] Columns;

    /**
     * gets isdefault
     * @return
     */
    public Boolean getIsDefault() {
        return IsDefault;
    }

    /**
     * sets isdefault
     * @param isDefault
     */
    public void setIsDefault(Boolean isDefault) {
        this.IsDefault = isDefault;
    }

    /**
     * gets columns
     * @return
     */
    public DataviewMappingColumn[] getColumns() {
        return Columns;
    }

    /**
     * sets columns
     * @param columns
     */
    public void setColumns(DataviewMappingColumn[] columns) {
        this.Columns = columns;
    }
}
