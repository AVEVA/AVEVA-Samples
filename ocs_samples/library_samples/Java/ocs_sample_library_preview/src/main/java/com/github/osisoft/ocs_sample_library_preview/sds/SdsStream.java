/** SdsStream.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

import java.util.List;

/**
 * SdsStream
 */
public class SdsStream {
    private String Id;
    private String Name;
    private String Description;
    private String TypeId;
    private SdsInterpolationMode InterpolationMode;
    private SdsStreamExtrapolation ExtrapolationMode;
    private List<SdsStreamPropertyOverride> PropertyOverrides;
    private List<SdsTypeProperty> Properties;
    private List<SdsStreamIndex> Indexes;

    /**
     * base constructor
     * @param id sets the name and id to this
     * @param typeid
     */
    public SdsStream(String id, String typeid) {
        this.Id = id;
        this.Name = id;
        this.TypeId = typeid;
    }

    /**
     * 
     * @param id sets the name and id to this
     * @param typeid
     * @param description
     */
    public SdsStream(String id, String typeid, String description) {
        this.Id = id;
        this.Name = id;
        this.TypeId = typeid;
        this.Description = description;
    }

    /**
     * 
     * @param id
     * @param typeid
     * @param description
     * @param name
     */
    public SdsStream(String id, String typeid, String description, String name) {
        this.Id = id;
        this.Name = name;
        this.TypeId = typeid;
        this.Description = description;
    }

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
     * gets typeid
     * @return
     */
    public String getTypeId() {
        return TypeId;
    }

    /**
     * sets typeid
     * @param typeId
     */
    public void setTypeId(String typeId) {
        TypeId = typeId;
    }

    /**
     * gets interpolationmode 
     * @return
     */
    public SdsInterpolationMode getInterpolationMode() {
        return InterpolationMode;
    }

    /**
     * sets interpolationmode
     * @param interpolationMode
     */
    public void setInterpolationMode(SdsInterpolationMode interpolationMode) {
        InterpolationMode = interpolationMode;
    }

    /**
     * gets extrapolationmode
     * @return
     */
    public SdsStreamExtrapolation getExtrapolationMode() {
        return ExtrapolationMode;
    }

    /**
     * sets extrapolationmode
     * @param extrapolationMode
     */
    public void setExtrapolationMode(SdsStreamExtrapolation extrapolationMode) {
        ExtrapolationMode = extrapolationMode;
    }

    /**
     * gets propertyoverrides
     * @return
     */
    public List<SdsStreamPropertyOverride> getPropertyOverrides() {
        return PropertyOverrides;
    }

    /**
     * sets propertyoverrides
     * @param propertyOverrides
     */
    public void setPropertyOverrides(List<SdsStreamPropertyOverride> propertyOverrides) {
        this.PropertyOverrides = propertyOverrides;
    }

    /**
     * gets properties
     * @return
     */
    public List<SdsTypeProperty> getProperties() {
        return Properties;
    }

    /**
     * sets properties
     * @param properties
     */
    public void setProperties(List<SdsTypeProperty> properties) {
        this.Properties = properties;
    }

    /**
     * gets indexes
     * @return
     */
    public List<SdsStreamIndex> getIndexes() {
        return Indexes;
    }

    /**
     * sets indexes
     * @param indexes
     */
    public void setIndexes(List<SdsStreamIndex> indexes) {
        this.Indexes = indexes;
    }
}
