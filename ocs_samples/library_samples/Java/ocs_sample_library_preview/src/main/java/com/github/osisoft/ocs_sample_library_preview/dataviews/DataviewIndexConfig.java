/** DataviewIndexConfig.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;

/**
 * DataviewIndexConfig
 */
public class DataviewIndexConfig {

    private Boolean IsDefault = true;
    private String StartIndex = "";
    private String EndIndex = "";
    private String Mode = "";
    private String Interval = "";

    /**
     * gets is default
     * @return
     */
    public Boolean getIsDefault() {
        return IsDefault;
    }

    /**
     * sets is default
     * @param isDefault
     */
    public void setIsDefault(Boolean isDefault) {
        this.IsDefault = isDefault;
    }

    /**
     * gets startindex
     * @return
     */
    public String getStartIndex() {
        return StartIndex;
    }

    /**
     * sets startindex
     * @param startIndex
     */
    public void setStartIndex(String startIndex) {
        this.StartIndex = startIndex;
    }

    /**
     * gets endindex
     * @return
     */
    public String getEndIndex() {
        return EndIndex;
    }

    /**
     * sets endindex
     * @param endIndex
     */
    public void setEndIndex(String endIndex) {
        this.EndIndex = endIndex;
    }

    /**
     * gets mode
     * @return
     */
    public String getMode() {
        return Mode;
    }

    /**
     * sets mode
     * @param mode
     */
    public void setMode(String mode) {
        this.Mode = mode;
    }

    /**
     * gets interval
     * @return
     */
    public String getInterval() {
        return Interval;
    }

    /**
     * sets interval
     * @param interval
     */
    public void setInterval(String interval) {
        this.Interval = interval;
    }

}
