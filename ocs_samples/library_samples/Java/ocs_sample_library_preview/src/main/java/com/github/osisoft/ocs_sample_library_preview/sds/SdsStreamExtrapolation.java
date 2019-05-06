/** SdsStreamExtrapolation.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/** 
 * SdsStreamExtrapolation 0-3
 */
public enum SdsStreamExtrapolation {

    All(0),
    None(1),
    Forward(2),
    Backward(3);

    private final int SdsStreamExtrapolation;

    private SdsStreamExtrapolation(int id) {
        this.SdsStreamExtrapolation = id;
    }

    /**
     * gets the value
     * @return
     */
    int getValue() {
        return SdsStreamExtrapolation;
    }
}
