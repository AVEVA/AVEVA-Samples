/** SdsType.java
 * 
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
