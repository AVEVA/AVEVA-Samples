package samples;


public class SdsViewMap {

    private String SourceTypeId = "";
    private String TargetTypeId = "";
    private SdsViewProperty[] Properties = new SdsViewProperty[0];

    public String getSourceTypeId() {
        return this.SourceTypeId;
    }

    public void setSourceTypeId(String sourceTypeId) {
        this.SourceTypeId = sourceTypeId;
    }
    
    public String getTargetTypeId() {
        return TargetTypeId;
    }

    public void setTargetTypeId(String targetTypeId) {
        this.TargetTypeId = targetTypeId;
    }

    public SdsViewProperty[] getProperties() {
        return Properties;
    }

    public void setProperties(SdsViewProperty[] properties) {
        this.Properties = properties;
    }
    
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("  SourceId = " + SourceTypeId);
        builder.append(", TargetId = " + TargetTypeId);        
        for(SdsViewProperty prop: Properties)
        {
        	if(prop.getTargetId() != null)
        	{
        	 builder.append(", SdsViewProperty: " + prop.getSourceId() + " => " + prop.getTargetId());
        	}
        }
       
        return builder.toString();
    }
}
