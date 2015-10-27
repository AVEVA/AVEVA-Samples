
module.exports = {
	qiTypeCodeMap : {
	        Empty : 0,
	        "Object" : 1,
	        DBNull : 2,
	        "Boolean" : 3,
	        Char : 4,
	        SByte : 5,
	        Byte : 6,
	        Int16 : 7,
	        UInt16 : 8,
	        Int32 : 9,
	        UInt32 : 10,
	        Int64 : 11,
	        UInt64 : 12,
	        Single : 13,
	        Double : 14,
	        Decimal : 15,
	        DateTime : 16,
	        "String" : 18,
	        Guid : 19,
	        DateTimeOffset : 20,
	        TimeSpan : 21,
	        Version : 22    
		},

	qiBoundaryType : {
			Exact : 0,
		    Inside : 1,
		    Outside : 2,
		    ExactOrCalculated : 3
	},

	qiStreamMode : {
			Continuous : 0,
		    StepwiseContinuousLeading : 1,
		    StepwiseContinuousTrailing : 2,
		    Discrete : 3,
		    Default : 0
	},

	//Qi Type

	QiType : function (qiType){
		if(qiType.Id){
			this.Id = qiType.Id
		}
		if(qiType.Name){
			this.Name = qiType.Name;
		}
		if(qiType.Description){
			this.Description = qiType.Description;
		}
		if(qiType.QiTypeCode){ 
			this.QiTypeCode = qiType.QiTypeCode;
		}
		if(qiType.Properties){
			this.Properties = qiType.Properties;
		}
	},


	//Qi Type Property

	QiTypeProperty : function (qiTypeProperty){
		if(qiTypeProperty.Id){
			this.Id = qiTypeProperty.Id;
		}
		if(qiTypeProperty.Name){
			this.Name = qiTypeProperty.Name;
		}
		if(qiTypeProperty.Description){
			this.Description = qiTypeProperty.Description;
		}
		if(qiTypeProperty.QiType){
			this.QiType = qiTypeProperty.QiType;
		}
		if(qiTypeProperty.IsKey){
			this.IsKey = qiTypeProperty.IsKey;
		}
	},


	//Qi Stream Object

	QiStream : function(qiStream){
		this.Id = qiStream.Id;
		this.Name = qiStream.Name;
		this.Description = qiStream.Description;
		this.TypeId = qiStream.TypeId;
		if(qiStream.BehaviorId){
			this.BehaviorId = qiStream.BehaviorId;
		}
	},

	//Qi Behavior object
	QiBehavior : function(qiBehavor){
		this.Id = null;
		this.Name = null;
		this.Mode = qiBehavor.Mode;
		this.ExtrapolationMode = null;
		this.Overrides = [];
	},


	//Wave Data Object

	WaveData : function (){
		this.Order = null;
	    this.Radians = null;
	    this.Tau = null;
	    this.Sin = null;
	    this.Cos = null;
	    this.Tan = null;
	    this.Sinh = null;
	    this.Cosh = null;
	    this.Tanh = null;
	},


	NextWave : function (interval, multiplier, order){
	    	now = new Date();
	    	midnight = new Date();
	    	midnight.setHours(0,0,0,0);
	    	totalSecondsDay = (now - midnight);
	    	_interval = (interval - midnight);
	    	radians = ((totalSecondsDay % _interval) / _interval) * 2 * Math.PI;

	    	newWave = new this.WaveData();
	    	newWave.Order = order;
		    newWave.Radians = radians;
		    newWave.Tau = radians / (2* Math.PI);
		    newWave.Sin = multiplier * Math.sin(radians);
		    newWave.Cos = multiplier * Math.cos(radians);
		    newWave.Tan = multiplier * Math.tan(radians);
		    newWave.Sinh = multiplier * Math.sinh(radians);
		    newWave.Cosh = multiplier * Math.cosh(radians);
		    newWave.Tanh = multiplier * Math.tanh(radians);

		    return newWave;
	}
}