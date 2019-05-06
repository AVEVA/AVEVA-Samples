/** DataviewQuery.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;

/**
 * DataviewQuery
 */
public class DataviewQuery {

    private String Id = "";
    private DataviewQueryQuery Query;

    /**
     * base constructor
     */
    public DataviewQuery( )
    {
        this.Query = new DataviewQueryQuery();
    }

    /**
     * generate the query from passed in values
     * @param Id 
     * @param Resource query resource can be something like "Streams", "TypeProperties"   required
     * @param Field query field can be something like "Id", "Name", "Tag", "Description", "TypeId", "MetadataKey"   required
     * @param Value value for field to use in query   required
     * @param Function  QueryFunction can be something like "Contains", "Equals", "EndsWith", "StartsWith"    required
     */
    public DataviewQuery(String Id, String Resource, String Field, String Value, String Function )
    {
        this.Id = Id;
        this.Query = new DataviewQueryQuery(Resource, Field, Value, Function);
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
    public DataviewQueryQuery getQuery() {
        return Query;
    }

    /**
     * sets query
     * @param query
     */
    public void setQuery(DataviewQueryQuery query) {
        this.Query = query;
    }
}
