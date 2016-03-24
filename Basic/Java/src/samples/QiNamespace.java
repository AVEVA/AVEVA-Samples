package samples;

public class QiNamespace 
{
    private String Id;
    
    public QiNamespace() 
    {
        this.Id = "Default";
    }
    
    public QiNamespace(String namespaceId) 
    {
        this.Id = namespaceId;
    }
    
    public String getId() 
    {
        return this.Id;
    }
    
    public void setId(String namespaceId) 
    {
        this.Id = namespaceId;
    }
}
