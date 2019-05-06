/** SdsStreamView.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/**
 * SdsStreamView
 */
public class SdsStreamView {

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private String SourceTypeId = "";
    private String TargetTypeId = "";
    private SdsStreamViewProperty[] Properties = new SdsStreamViewProperty[0];

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
     * gets SourceTypeId
     * @return
     */
    public String getSourceTypeId() {
        return this.SourceTypeId;
    }

    /**
     * sets SourceTypeId
     * @param sourceTypeId
     */
    public void setSourceTypeId(String sourceTypeId) {
        this.SourceTypeId = sourceTypeId;
    }
    
    /**
     * gets TargetTypeId
     * @return
     */
    public String getTargetTypeId() {
        return TargetTypeId;
    }

    /**
     * sets TargetTypeId
     * @param targetTypeId
     */
    public void setTargetTypeId(String targetTypeId) {
        this.TargetTypeId = targetTypeId;
    }

    /**
     * gets properties
     * @return
     */
    public SdsStreamViewProperty[] getProperties() {
        return Properties;
    }

    /**
     * sets properties
     * @param properties
     */
    public void setProperties(SdsStreamViewProperty[] properties) {
        this.Properties = properties;
    }
}
