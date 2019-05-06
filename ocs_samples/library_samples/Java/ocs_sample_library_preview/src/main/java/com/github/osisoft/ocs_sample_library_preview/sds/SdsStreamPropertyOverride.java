/** SdsStreamPropertyOverride.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/**
 * SdsStreamPropertyOverride
 */
public class SdsStreamPropertyOverride {
    private String sdsTypePropertyId;
    private SdsInterpolationMode interpolationMode;
    private String uom;
    
    /**
     * baseconstructor
     */
    public SdsStreamPropertyOverride() {

    }
    /**
     * gets sdsTypePropertyId
     * @return
     */
    public String getSdsTypePropertyId() {
        return sdsTypePropertyId;
    }

    /**
     * sets sdsTypePropertyId   
     * @param sdsTypePropertyId
     */
    public void setSdsTypePropertyId(String sdsTypePropertyId) {
        this.sdsTypePropertyId = sdsTypePropertyId;
    }

    /**
     * gets interpolationMode
     * @return
     */
    public SdsInterpolationMode getInterpolationMode() {
        return interpolationMode;
    }

    /**
     * sets interpolationMode
     * @param interpolationMode
     */
    public void setInterpolationMode(SdsInterpolationMode interpolationMode) {
        this.interpolationMode = interpolationMode;
    }
    
    /**
     * gets unit of measure
     * @return
     */
    public String getUom() {
        return uom;
    }

    /**
     * sets unit of measure
     * @param uom
     */
    public void setUom(String uom) {
        this.uom = uom;
    }
}
