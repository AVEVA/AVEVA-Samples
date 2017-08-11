package samples;


public class QiType {

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private QiTypeCode QiTypeCode;
    private QiTypeProperty[] Properties = new QiTypeProperty[0];

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

    public QiTypeCode getQiTypeCode() {
        return QiTypeCode;
    }

    public void setQiTypeCode(QiTypeCode qiTypeCode) {
        this.QiTypeCode = qiTypeCode;
    }

    public QiTypeProperty[] getProperties() {
        return Properties;
    }

    public void setProperties(QiTypeProperty[] properties) {
        this.Properties = properties;
    }
}
