/** SdsTypeProperty.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/** 
 * SdsTypeProperty
 */
public class SdsTypeProperty {

    /**
     * base constructor
     */
    public SdsTypeProperty()
    {}

    /**
     * 
     * @param id
     * @param name
     * @param description
     * @param sdsType SdsType
     * @param isKey
     */
    public SdsTypeProperty(String id, String name, String description, SdsType sdsType, boolean isKey)
    {
        setName(name);
        setId(id);
        setDescription(description);
        setSdsType(sdsType);
        setIsKey(isKey);    
    }

    /**
     * 
     * @param id
     * @param name
     * @param description
     * @param sdsType
     * @param isKey
     * @param order include this if you have a compound index
     */
    public SdsTypeProperty(String id, String name, String description, SdsType sdsType, boolean isKey, int order)
    {
        setName(name);
        setId(id);
        setDescription(description);
        setSdsType(sdsType);
        setIsKey(isKey);    
        setOrder(order);    
    }

    private String Name;
    private String Id;
    private String Description;
    private SdsType SdsType;
    private boolean IsKey;
    private int Order;

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
     * gets sdstype
     * @return
     */
    public SdsType getSdsType() {
        return SdsType;
    }

    /**
     * sets sdstype
     * @param sdsType
     */
    public void setSdsType(SdsType sdsType) {
        this.SdsType = sdsType;
    }

    /**
     * gets iskey
     * @return
     */
    public boolean getIsKey() {
        return IsKey;
    }

    /**
     * sets iskey
     * @param isKey
     */
    public void setIsKey(boolean isKey) {
        IsKey = isKey;
    }

    /**
     * gets order.  used for complex indexed type
     * @return
     */
    public int getOrder() {
        return Order;
    }

    /**
     * sets order.   used for complex indexed type
     * @param order
     */
    public void setOrder(int order) {
        Order = order;
    }
    
}
