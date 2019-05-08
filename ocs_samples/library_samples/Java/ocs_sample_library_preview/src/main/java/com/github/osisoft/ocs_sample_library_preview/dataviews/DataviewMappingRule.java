/** DataviewMappingRule.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;

import java.util.Map;

/**
 * DataviewMappingRule
 */
public class DataviewMappingRule {

    private String[] PropertyPaths;
    private String GroupRuleId = "";

    /**
     * gets property paths
     * @return
     */
    public String[] getPropertyPaths() {
        return PropertyPaths;
    }

    /**
     * sets propertypaths
     * @param propertyPaths
     */
    public void setPropertyPaths(String[] propertyPaths) {
        this.PropertyPaths = propertyPaths;
    }

    /**
     * gets groupruleid
     * @return
     */
    public String getGroupRuleId() {
        return GroupRuleId;
    }

    /**
     * sets groupruleid
     * @param groupRuleId
     */
    public void setGroupRuleId(String groupRuleId) {
        this.GroupRuleId = groupRuleId;
    }
}
