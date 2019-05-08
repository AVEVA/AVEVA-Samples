/** SdsStreamViewMap.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/**
 * SdsStreamViewMap
 */
public class SdsStreamViewMap {

    private String SourceTypeId = "";
    private String TargetTypeId = "";
    private SdsStreamViewProperty[] Properties = new SdsStreamViewProperty[0];

    /**
     * gets SourceTypeId
     * @return
     */
    public String getSourceTypeId() {
        return this.SourceTypeId;
    }

    /**
     * sets SourceTypeId
     * @param sourceTypeId
     */
    public void setSourceTypeId(String sourceTypeId) {
        this.SourceTypeId = sourceTypeId;
    }
    
    /**
     * gets TargetTypeId
     * @return
     */
    public String getTargetTypeId() {
        return TargetTypeId;
    }

    /**
     * sets TargetTypeId
     * @param targetTypeId
     */
    public void setTargetTypeId(String targetTypeId) {
        this.TargetTypeId = targetTypeId;
    }

    /**
     * gets Properties
     * @return
     */
    public SdsStreamViewProperty[] getProperties() {
        return Properties;
    }

    /**
     * sets Properties
     * @param properties
     */
    public void setProperties(SdsStreamViewProperty[] properties) {
        this.Properties = properties;
    }
    
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("  SourceId = " + SourceTypeId);
        builder.append(", TargetId = " + TargetTypeId);        
        for(SdsStreamViewProperty prop: Properties)
        {
        	if(prop.getTargetId() != null)
        	{
        	 builder.append(", SdsStreamViewProperty: " + prop.getSourceId() + " => " + prop.getTargetId());
        	}
        }
       
        return builder.toString();
    }
}
