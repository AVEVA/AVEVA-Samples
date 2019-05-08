/** SdsInterpolationMode.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/**
 * SdsInterpolationMode 0-3
 */
public enum SdsInterpolationMode {

    Continuous(0),
    StepwiseContinuousLeading(1),
    StepwiseContinuousTrailing(2),
    Discrete(3);
    private final int SdsInterpolationMode;

    private SdsInterpolationMode(int id) {
        this.SdsInterpolationMode = id;
    }
    
    /**
     * gets the int value
     * @return
     */
    public int getValue() {
        return SdsInterpolationMode;
    }
}
