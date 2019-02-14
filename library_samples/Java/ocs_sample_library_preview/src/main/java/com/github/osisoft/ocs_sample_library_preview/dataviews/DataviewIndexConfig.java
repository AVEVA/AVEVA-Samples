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


public class DataviewIndexConfig {

    private String IsDefault = "";
    private String StartIndex = "";
    private String EndIndex = "";
    private String Mode = "";
    private String Interval = "";

    public String getIsDefault() {
        return IsDefault;
    }

    public void setIsDefault(String isDefault) {
        this.IsDefault = isDefault;
    }

    public String getStartIndex() {
        return StartIndex;
    }

    public void setStartIndex(String startIndex) {
        this.StartIndex = startIndex;
    }

    public String getEndIndex() {
        return EndIndex;
    }

    public void setEndIndex(String endIndex) {
        this.EndIndex = endIndex;
    }

    public String getMode() {
        return Mode;
    }

    public void setMode(String mode) {
        this.Mode = mode;
    }

    public String getInterval() {
        return Interval;
    }

    public void setInterval(String interval) {
        this.Interval = interval;
    }

}
