package samples;


public class SdsType {

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private SdsTypeCode SdsTypeCode;
    private SdsTypeProperty[] Properties = new SdsTypeProperty[0];

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

    public SdsTypeCode getSdsTypeCode() {
        return SdsTypeCode;
    }

    public void setSdsTypeCode(SdsTypeCode sdsTypeCode) {
        this.SdsTypeCode = sdsTypeCode;
    }

    public SdsTypeProperty[] getProperties() {
        return Properties;
    }

    public void setProperties(SdsTypeProperty[] properties) {
        this.Properties = properties;
    }
}
