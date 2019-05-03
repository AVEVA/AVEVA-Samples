/** SdsType.java
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

package  com.github.osisoft.ocs_sample_library_preview.sds;

/**
 * SdsType
 */
public class SdsType {

    /**
     * Base Constructors
     */
    public SdsType ()
    {

    } 

    /**
     * 
     * @param id
     * @param name
     * @param description
     * @param sdsTypeCode SdsTypeCode
     */
    public SdsType (String id, String name, String description, SdsTypeCode sdsTypeCode)
    {
        setId(id);
        setName(name);
        setDescription(description);
        setSdsTypeCode(sdsTypeCode);
    } 

    /**
     * 
     * @param id
     * @param name
     * @param description
     * @param sdsTypeCode SdsTypeCode
     * @param properties  SdsTypeProperty[] 
     */
    public SdsType (String id, String name, String description, SdsTypeCode sdsTypeCode, SdsTypeProperty[] properties)
    {
        setId(id);
        setName(name);
        setDescription(description);
        setSdsTypeCode(sdsTypeCode);
        setProperties(properties);
    } 

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private SdsTypeCode SdsTypeCode;
    private SdsTypeProperty[] Properties = new SdsTypeProperty[0];

    /**
     * gets id
     * @return
     */
    public String getId() {
        return Id;
    }

    /**
     * sets id
     * @param id
     */
    public void setId(String id) {
        this.Id = id;
    }

    /**
     * gets name
     * @return
     */
    public String getName() {
        return Name;
    }

    /**
     * sets name
     * @param name
     */
    public void setName(String name) {
        this.Name = name;
    }

    /**
     * gets description
     * @return
     */
    public String getDescription() {
        return Description;
    }

    /**
     * sets description
     * @param description
     */
    public void setDescription(String description) {
        this.Description = description;
    }

    /**
     * gets SdsTypeCode
     * @return  
     */
    public SdsTypeCode getSdsTypeCode() {
        return SdsTypeCode;
    }

    /**
     *  sets SdsTypeCode
     * @param sdsTypeCode
     */
    public void setSdsTypeCode(SdsTypeCode sdsTypeCode) {
        this.SdsTypeCode = sdsTypeCode;
    }

    /**
     * gets properties
     * @return
     */
    public SdsTypeProperty[] getProperties() {
        return Properties;
    }

    /**
     * sets properties
     * @param properties
     */
    public void setProperties(SdsTypeProperty[] properties) {
        this.Properties = properties;
    }
}
