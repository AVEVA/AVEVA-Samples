package samples;


public class SdsTypeProperty {
    private String Name;
    private String Id;
    private String Description;
    private SdsType SdsType;
    private boolean IsKey;

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getDescription() {
        return Description;
    }

    public void setDescription(String description) {
        this.Description = description;
    }

    public SdsType getSdsType() {
        return SdsType;
    }

    public void setSdsType(SdsType sdsType) {
        this.SdsType = sdsType;
    }

    public boolean isIsKey() {
        return IsKey;
    }

    public void setIsKey(boolean isKey) {
        IsKey = isKey;
    }
}
