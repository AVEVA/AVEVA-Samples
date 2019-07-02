/** DataviewQuery.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;

/**
 * DataviewQuery
 */
public class DataviewQuery {

    private String Id = "";
    private String Query = "";

    /**
     * base constructor
     */
    public DataviewQuery( )
    {

    }
    /**
     * Constructor
     */
    public DataviewQuery(String id, String query )
    {
        Id= id;
        Query= query;
    }

    /**
     * gets id
     * @return
     */
    public String getId() {
        return Id;
    }

    /**
     * sets id
     * @param id
     */
    public void setId(String id) {
        this.Id = id;
    }

    /**
     * gets query
     * @return
     */
    public String getQuery() {
        return Query;
    }

    /**
     * sets query
     * @param query
     */
    public void setQuery(String query) {
        this.Query = query;
    }
}
