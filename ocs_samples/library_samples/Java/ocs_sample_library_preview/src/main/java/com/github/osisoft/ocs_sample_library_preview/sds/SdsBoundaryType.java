/** SdsBoundaryType.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/**
 * SdsBoundaryType 0-3
 */
public enum SdsBoundaryType {

    Exact(0),
    Inside(1),
    Outside(2),
    ExactOrCalculated(3);

    private final int SdsBoundaryType;

    private SdsBoundaryType(int id) {
        this.SdsBoundaryType = id;
    }

    /**
     * gets the int value
     * @return
     */
    public int getValue() {
        return SdsBoundaryType;
    }
}
