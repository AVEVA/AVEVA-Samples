/** DataviewMappingColumn.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;


/**
 * DataviewMappingColumn
 */
public class DataviewMappingColumn {

    private String Name = "";
    private String IsKey = "";
    private String DataType = "";
    private DataviewMappingRule MappingRule;

    /**
     * gets name
     * @return
     */
    public String getName() {
        return Name;
    }

    /**
     * sets name
     * @param name
     */
    public void setName(String name) {
        this.Name = name;
    }

    /**
     * get iskey
     * @return
     */
    public String getIsKey() {
        return IsKey;
    }

    /**
     * sets is key
     * @param isKey
     */
    public void setIsKey(String isKey) {
        this.IsKey = isKey;
    }

    /**
     * gets datatype
     * @return
     */
    public String getDataType() {
        return DataType;
    }

    /**
     * sets datatype
     * @param dataType
     */
    public void setDataType(String dataType) {
        this.DataType = dataType;
    }

    /**
     * gets mappingrule
     * @return
     */
    public DataviewMappingRule  getMappingRule() {
        return MappingRule;
    }

    /**
     * sets mappingrule
     * @param mappingRule
     */
    public void setMappingRule(DataviewMappingRule mappingRule) {
        this.MappingRule = mappingRule;
    }
}
