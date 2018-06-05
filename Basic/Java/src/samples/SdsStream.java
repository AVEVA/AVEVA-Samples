package samples;

import java.util.List;

public class SdsStream {
    private String Id;
    private String Name;
    private String Description;
    private String TypeId;
    private SdsInterpolationMode InterpolationMode;
    private SdsStreamExtrapolation ExtrapolationMode;
    private List<SdsStreamPropertyOverride> PropertyOverrides;
    private List<SdsTypeProperty> Properties;

    public SdsStream(String name, String typeid) {
        this.Id = name;
        this.Name = name;
        this.TypeId = typeid;
    }

    public SdsStream(String name, String typeid, String description, String behavior) {
        this.Id = name;
        this.Name = name;
        this.TypeId = typeid;
        this.Description = description;
    }

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

    public String getTypeId() {
        return TypeId;
    }

    public void setTypeId(String typeId) {
        TypeId = typeId;
    }

    public SdsInterpolationMode getInterpolationMode() {
        return InterpolationMode;
    }

    public void setInterpolationMode(SdsInterpolationMode interpolationMode) {
        InterpolationMode = interpolationMode;
    }

    public SdsStreamExtrapolation getExtrapolationMode() {
        return ExtrapolationMode;
    }

    public void setExtrapolationMode(SdsStreamExtrapolation extrapolationMode) {
        ExtrapolationMode = extrapolationMode;
    }

    public List<SdsStreamPropertyOverride> getPropertyOverrides() {
        return PropertyOverrides;
    }

    public void setPropertyOverrides(List<SdsStreamPropertyOverride> propertyOverrides) {
        this.PropertyOverrides = propertyOverrides;
    }

    public List<SdsTypeProperty> getProperties() {
        return Properties;
    }

    public void setProperties(List<SdsTypeProperty> properties) {
        this.Properties = properties;
    }
}
