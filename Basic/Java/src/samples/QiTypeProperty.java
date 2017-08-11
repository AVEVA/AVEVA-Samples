package samples;


public class QiTypeProperty {
    private String Name;
    private String Id;
    private String Description;
    private QiType QiType;
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

    public QiType getQiType() {
        return QiType;
    }

    public void setQiType(QiType qiType) {
        this.QiType = qiType;
    }

    public boolean isIsKey() {
        return IsKey;
    }

    public void setIsKey(boolean isKey) {
        IsKey = isKey;
    }
}
