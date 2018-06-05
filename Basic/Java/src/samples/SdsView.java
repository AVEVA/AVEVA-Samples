package samples;


public class SdsView {

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private String SourceTypeId = "";
    private String TargetTypeId = "";
    private SdsViewProperty[] Properties = new SdsViewProperty[0];

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

    public String getSourceTypeId() {
        return this.SourceTypeId;
    }

    public void setSourceTypeId(String sourceTypeId) {
        this.SourceTypeId = sourceTypeId;
    }
    
    public String getTargetTypeId() {
        return TargetTypeId;
    }

    public void setTargetTypeId(String targetTypeId) {
        this.TargetTypeId = targetTypeId;
    }

    public SdsViewProperty[] getProperties() {
        return Properties;
    }

    public void setProperties(SdsViewProperty[] properties) {
        this.Properties = properties;
    }
}
