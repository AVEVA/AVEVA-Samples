/** Datagroups.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;

import java.util.Map;

/**
 * Collection of Datagroups
 */
public class Datagroups {
    
    private Map<String,Datagroup> DataGroups;


    /**
     * gets the collection of datagroups
     * @return datagroups
     */
    public Map<String,Datagroup>  getDataGroups() {
        return DataGroups;
    }

    /**
     * sets the collection of datagroups
     * @param dataGroups datagroups to set
     */
    public void setDataGroups(Map<String,Datagroup> dataGroups) {
        this.DataGroups = dataGroups;
    }
}
