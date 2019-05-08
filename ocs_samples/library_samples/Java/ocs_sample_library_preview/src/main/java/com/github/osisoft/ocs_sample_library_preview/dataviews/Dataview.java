/** Dataview.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.dataviews;

/**
 * Object to heklp with doing ML tasks against OCS
 */
public class Dataview {

    private String Id = "";
    private String Name = "";
    private String Description = "";
    private DataviewQuery[] Queries;
    private DataviewGroupRule[] GroupRules;
    private DataviewMapping Mappings;
    private DataviewIndexConfig IndexConfig;
    private String IndexDataType = "";

    /**
     * Base constructor
     */
    public Dataview()
    {
        this.Mappings =  new DataviewMapping();
    }

    /**
     * constructor
     * @param Id  Required
     * @param Queries DataviewQuery[]  Required
     * @param GroupRules DataviewGroupRule[]   Required
     * @param IndexDataType Limited to "DateTime" currently   Required  
     */
    public Dataview(String Id, DataviewQuery[] Queries, DataviewGroupRule[] GroupRules,String IndexDataType)
    {
        this.Id = Id;
        this.Queries = Queries;
        this.GroupRules = GroupRules;
        this.Mappings = new DataviewMapping();
        this.IndexDataType = IndexDataType;
    }

    /**
     * consturctor
     * @param Id  Required
     * @param Name not required
     * @param Description not required
     * @param Queries DataviewQuery[]  Required
     * @param GroupRules DataviewGroupRule[]   Required
     * @param IndexDataType Limited to "DateTime" currently   Required  
     */
    public Dataview(String Id ,String Name, String Description, DataviewQuery[] Queries, DataviewGroupRule[] GroupRules,String IndexDataType)
    {
        this.Id = Id;
        this.Queries = Queries;
        this.GroupRules = GroupRules;
        this.Mappings = new DataviewMapping();
        this.IndexDataType = IndexDataType;
    }

    /**
     * consturctor
     * @param Id  Required
     * @param Name not required
     * @param Description not required
     * @param Queries DataviewQuery[]  Required
     * @param GroupRules DataviewGroupRule[]   Required
     * @param Mappings DataviewMapping required
     * @param IndexConfig DataviewIndexConfig   not require
     * @param IndexDataType Limited to "DateTime" currently    Required  
     */
    public Dataview(String Id, String Name, String Description, DataviewQuery[] Queries, DataviewGroupRule[] GroupRules, DataviewMapping Mappings, DataviewIndexConfig IndexConfig,String IndexDataType)
    {
        this.Id = Id;
        this.Name = Name;
        this.Description = Description;
        this.Queries = Queries;
        this.GroupRules = GroupRules;
        this.Mappings = Mappings;
        this.IndexConfig = IndexConfig;
        this.IndexDataType = IndexDataType;
    }

    /**
     * Gets id
     * @return id
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
     * gets description
     * @return
     */
    public String getDescription() {
        return Description;
    }

    /**
     * sets description
     * @param description
     */
    public void setDescription(String description) {
        this.Description = description;
    }

    /**
     * get quieres
     * @return  DataviewQuery[]
     */
    public DataviewQuery[] getQueries() {
        return Queries;
    }

    /**
     * set queries
     * @param queries DataviewQuery[] 
     */
    public void setQueries(DataviewQuery[] queries) {
        this.Queries = queries;
    }

    /**
     * gets mappings 
     * @return DataviewMapping
     */
    public DataviewMapping getMappings() {
        return Mappings;
    }

    /**
     * set mappings
     * @param mappings DataviewMapping
     */
    public void setMappings(DataviewMapping mappings) {
        this.Mappings = mappings;
    }

    /**
     * gets indexconfig
     * @return DataviewIndexConfig
     */
    public DataviewIndexConfig getIndexConfig() {
        return IndexConfig;
    }

    /**
     * sets indexconfig
     * @param indexConfig DataviewIndexConfig
     */
    public void setIndexConfig(DataviewIndexConfig indexConfig) {
        this.IndexConfig = indexConfig;
    }

    /**
     * gets indexdatatype
     * @return
     */
    public String getIndexDataType() {
        return IndexDataType;
    }

    /**
     * sets indexdatatype
     * @param indexDataType
     */
    public void setIndexDataType(String indexDataType) {
        this.IndexDataType = indexDataType;
    }
        
    /**
     * gets group rules
     * @return DataviewGroupRule[] 
     */
    public DataviewGroupRule[]  getGroupRules() {
        return GroupRules;
    }
    /**
     * sets group rules
     * @param rules
     */
    public void setGroupRules(DataviewGroupRule[]  rules) {
        this.GroupRules = rules;
    }
}
