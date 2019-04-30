/** DataviewIndexConfig.java
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
 * DataviewIndexConfig
 */
public class DataviewIndexConfig {

    private Boolean IsDefault = true;
    private String StartIndex = "";
    private String EndIndex = "";
    private String Mode = "";
    private String Interval = "";

    /**
     * gets is default
     * @return
     */
    public Boolean getIsDefault() {
        return IsDefault;
    }

    /**
     * sets is default
     * @param isDefault
     */
    public void setIsDefault(Boolean isDefault) {
        this.IsDefault = isDefault;
    }

    /**
     * gets startindex
     * @return
     */
    public String getStartIndex() {
        return StartIndex;
    }

    /**
     * sets startindex
     * @param startIndex
     */
    public void setStartIndex(String startIndex) {
        this.StartIndex = startIndex;
    }

    /**
     * gets endindex
     * @return
     */
    public String getEndIndex() {
        return EndIndex;
    }

    /**
     * sets endindex
     * @param endIndex
     */
    public void setEndIndex(String endIndex) {
        this.EndIndex = endIndex;
    }

    /**
     * gets mode
     * @return
     */
    public String getMode() {
        return Mode;
    }

    /**
     * sets mode
     * @param mode
     */
    public void setMode(String mode) {
        this.Mode = mode;
    }

    /**
     * gets interval
     * @return
     */
    public String getInterval() {
        return Interval;
    }

    /**
     * sets interval
     * @param interval
     */
    public void setInterval(String interval) {
        this.Interval = interval;
    }

}
