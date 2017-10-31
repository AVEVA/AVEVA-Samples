package samples;


public class QiViewProperty {
    private String SourceId;
    private String TargetId;
    private QiView QiView;

    public String getSourceId() {
        return SourceId;
    }

    public void setSourceId(String SourceId) {
        this.SourceId = SourceId;
    }

    public String getTargetId() {
        return TargetId;
    }

    public void setTargetId(String targetId) {
        this.TargetId = targetId;
    }

    public QiView getQiView() {
        return QiView;
    }

    public void setQiView(QiView qiView) {
        this.QiView = qiView;
    }
}
