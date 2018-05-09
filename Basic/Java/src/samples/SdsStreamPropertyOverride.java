package samples;

public class SdsStreamPropertyOverride {
    private String sdsTypePropertyId;
    private SdsInterpolationMode interpolationModeOverride;
    private String uomOverride;
    
    public SdsStreamPropertyOverride() {

    }

    public String getSdsTypePropertyId() {
        return sdsTypePropertyId;
    }

    public void setSdsTypePropertyId(String sdsTypePropertyId) {
        this.sdsTypePropertyId = sdsTypePropertyId;
    }

    public SdsInterpolationMode getInterpolationModeOverride() {
        return interpolationModeOverride;
    }

    public void setInterpolationModeOverride(SdsInterpolationMode interpolationModeOverride) {
        this.interpolationModeOverride = interpolationModeOverride;
    }
    
    public String getUomOverride() {
        return uomOverride;
    }

    public void setUomOverride(String uomOverride) {
        this.uomOverride = uomOverride;
    }
}
