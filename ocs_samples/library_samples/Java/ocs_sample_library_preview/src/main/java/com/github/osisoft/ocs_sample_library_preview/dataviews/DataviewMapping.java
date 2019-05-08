/** DataviewMapping.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;

/**
 * DataviewMapping
 */
public class DataviewMapping {

    private Boolean IsDefault = true;
    private DataviewMappingColumn[] Columns;

    /**
     * gets isdefault
     * @return
     */
    public Boolean getIsDefault() {
        return IsDefault;
    }

    /**
     * sets isdefault
     * @param isDefault
     */
    public void setIsDefault(Boolean isDefault) {
        this.IsDefault = isDefault;
    }

    /**
     * gets columns
     * @return
     */
    public DataviewMappingColumn[] getColumns() {
        return Columns;
    }

    /**
     * sets columns
     * @param columns
     */
    public void setColumns(DataviewMappingColumn[] columns) {
        this.Columns = columns;
    }
}
