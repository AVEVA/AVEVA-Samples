package samples;


public class SdsViewProperty {
    private String SourceId;
    private String TargetId;
    private SdsView SdsView;

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

    public SdsView getSdsView() {
        return SdsView;
    }

    public void setSdsView(SdsView sdsView) {
        this.SdsView = sdsView;
    }
}
