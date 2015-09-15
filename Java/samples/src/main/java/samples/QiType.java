package samples;



public class QiType {

	private String Id;
	private String Name;
	private String Description;
	private QiTypeCode QiTypeCode;
	private QiTypeProperty[] Properties;
	// private List<QiTypeProperty> Properties;

	/*    
	   public QiType(){
			this.Id = "";
			this.Name = "NONE";
			this.Description = "NONE";
			this.QiTypeCode = QiTypeCode.Object;
			this.Properties = null;


		}
	 */
	public String getId() {
		return Id;
	}

	public void setId(String id) {
		this.Id = id;
	}

	public String getName() {
		return Name;
	}

	public void setName(String name) {
		this.Name = name;
	}

	public String getDescription() {
		return Description;
	}

	public void setDescription(String description) {
		this.Description = description;
	}

	public QiTypeCode getQiTypeCode() {
		return QiTypeCode;
	}

	public void setQiTypeCode(QiTypeCode qiTypeCode) {
		this.QiTypeCode = qiTypeCode;
	}

	public QiTypeProperty[] getProperties() {
		return Properties;
	}
	public void setProperties(QiTypeProperty[] properties) {
		this.Properties = properties;
	}


	/*		
		public List<QiTypeProperty> getProperties() {
			return Properties;
		}
		public void setProperties(List<QiTypeProperty> properties) {
			this.Properties = properties;
		}
	 */		


	/*	
		 public String toStringformat(){

		 Gson gson = new Gson();	

		 JsonObject js = new JsonObject();
         js.addProperty("Id",this.getId());
         js.addProperty("Name", this.getName());
         js.addProperty("Description", this.getDescription());
         js.addProperty("QiTypeCode",  gson.toJson(this.getQiTypeCode()));
         js.addProperty("Properties", gson.toJson(this.getProperties()) );
         String target = js.toString();

         System.out.println(target);

         return target;
		 }
	 */
}
