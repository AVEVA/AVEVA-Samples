package samples;


public class QiViewMap {

    private String SourceTypeId = "";
    private String TargetTypeId = "";
    private QiViewProperty[] Properties = new QiViewProperty[0];

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

    public QiViewProperty[] getProperties() {
        return Properties;
    }

    public void setProperties(QiViewProperty[] properties) {
        this.Properties = properties;
    }
    
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("  SourceId = " + SourceTypeId);
        builder.append(", TargetId = " + TargetTypeId);        
        for(QiViewProperty prop: Properties)
        {
        	if(prop.getTargetId() != null)
        	{
        	 builder.append(", QiViewProperty: " + prop.getSourceId() + " => " + prop.getTargetId());
        	}
        }
       
        return builder.toString();
    }
}
