package samples;

public class SdsStreamPropertyOverride {
    private String sdsTypePropertyId;
    private SdsInterpolationMode interpolationMode;
    private String uom;
    
    public SdsStreamPropertyOverride() {

    }

    public String getSdsTypePropertyId() {
        return sdsTypePropertyId;
    }

    public void setSdsTypePropertyId(String sdsTypePropertyId) {
        this.sdsTypePropertyId = sdsTypePropertyId;
    }

    public SdsInterpolationMode getInterpolationMode() {
        return interpolationMode;
    }

    public void setInterpolationMode(SdsInterpolationMode interpolationMode) {
        this.interpolationMode = interpolationMode;
    }
    
    public String getUom() {
        return uom;
    }

    public void setUom(String uom) {
        this.uom = uom;
    }
}
