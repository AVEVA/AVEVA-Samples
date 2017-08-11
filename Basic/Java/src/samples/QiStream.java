package samples;

import java.util.List;

public class QiStream {
    private String Id;
    private String Name;
    private String Description;
    private String TypeId;
    private String BehaviorId;
    private List<QiTypeProperty> Properties;

    public QiStream(String name, String typeid) {
        this.Id = name;
        this.Name = name;
        this.TypeId = typeid;
    }

    public QiStream(String name, String typeid, String description, String behavior) {
        this.Id = name;
        this.Name = name;
        this.TypeId = typeid;
        this.Description = description;
        this.BehaviorId = behavior;
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

    public String getBehaviorId() {
        return BehaviorId;
    }

    public void setBehaviorId(String behaviorId) {
        BehaviorId = behaviorId;
    }

    public List<QiTypeProperty> getProperties() {
        return Properties;
    }

    public void setProperties(List<QiTypeProperty> properties) {
        this.Properties = properties;
    }
}
