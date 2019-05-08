/** SdsStreamViewProperty.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/** 
 * SdsStreamViewProperty
 */
public class SdsStreamViewProperty {
    private String SourceId;
    private String TargetId;
    private SdsStreamView SdsStreamView;

    /**
     * gets SourceId
     * @return
     */
    public String getSourceId() {
        return SourceId;
    }

    /**
     * sets SourceId
     * @param SourceId
     */
    public void setSourceId(String SourceId) {
        this.SourceId = SourceId;
    }

    /**
     * gets targetid
     * @return
     */
    public String getTargetId() {
        return TargetId;
    }

    /**
     * sets targetid
     * @param targetId
     */
    public void setTargetId(String targetId) {
        this.TargetId = targetId;
    }

    /**
     * gets SdsStreamView
     * @return
     */
    public SdsStreamView getSdsStreamView() {
        return SdsStreamView;
    }

    /**
     * sets SdsStreamView
     * @param sdsStreamView
     */
    public void setSdsStreamView(SdsStreamView sdsStreamView) {
        this.SdsStreamView = sdsStreamView;
    }
}
