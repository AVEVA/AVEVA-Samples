package samples;

import java.util.List;

public class QiStreamBehavior {
    private String Id;
    private String Name;
    private QiStreamMode Mode;
    private QiStreamExtrapolation ExtrapolationMode;
    private List<QiStreamBehaviorOverride> Overrides;

    public QiStreamBehavior() {
        this.Mode = QiStreamMode.Continuous;

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

    public QiStreamMode getMode() {
        return Mode;
    }

    public void setMode(QiStreamMode mode) {
        this.Mode = mode;
    }

    public QiStreamExtrapolation getExtrapolationMode() {
        return ExtrapolationMode;
    }

    public void setExtrapolationMode(QiStreamExtrapolation extrapolationMode) {
        ExtrapolationMode = extrapolationMode;
    }

    public List<QiStreamBehaviorOverride> getOverrides() {
        return Overrides;
    }

    public void setOverrides(List<QiStreamBehaviorOverride> overrides) {
        this.Overrides = overrides;
    }
}
