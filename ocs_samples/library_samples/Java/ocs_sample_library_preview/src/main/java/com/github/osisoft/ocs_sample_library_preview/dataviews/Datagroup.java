/** Datagroup.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;
import java.util.Map;

/**
 * Datagroup object from a Dataview
 */
public class Datagroup {
    
    private Map<String,Object> Tokens;
    private Object DataItems;

    /**
     * Gets the tokens for the datagroup
     * @return the tokens for the datagroup
     */
    public Map<String,Object>  getTokens() {
        return Tokens;
    }

    /**
     * sets the tokens for the datagroup
     * @param tokens the tokens for the datagroup
     */
    public void setTokens(Map<String,Object> tokens) {
        this.Tokens = tokens;
    }
        
    /**
     * gets the dataitems for the datagroup
     * @return the dataitems
     */
    public Object getDataItems() {
        return DataItems;
    }

    /**
     * sets the dataitems for the datagroup
     * @param dataItems
     */
    public void setDataItems(Object dataItems) {
        this.DataItems = dataItems;
    }
}
