

//function to create client object
var qiObjs = require("./QiObjects.js");
var restCall = require("request-promise");

String.prototype.format = function (args) {
            var str = this;
            return str.replace(String.prototype.format.regex, function(item) {
                var intVal = parseInt(item.substring(1, item.length - 1));
                var replace;
                if (intVal >= 0) {
                    replace = args[intVal];
                } else if (intVal === -1) {
                    replace = "{";
                } else if (intVal === -2) {
                    replace = "}";
                } else {
                    replace = "";
                }
                return replace;
            });
        };
        String.prototype.format.regex = new RegExp("{-?[0-9]+}", "g");

module.exports = {
    QiClient : function(url){
        this.url = url;
        this.version = 0.1;
        this.tenantsBase = "/Qi/Tenants";
		this.namespacesBase = "/Qi/{0}/Namespaces"
        this.typesBase = "/Qi/{0}/{1}/Types";
        this.streamsBase = "/Qi/{0}/{1}/Streams";
        this.behaviorBase = "/Qi/{0}/{1}/Behaviors";
        this.insertSingle = "/Data/InsertValue";
        this.insertMultiple = "/Data/InsertValues";
        this.getTemplate = "/{0}/Data/GetWindowValues?startIndex={1}&endIndex={2}";
        this.getRangeTemplate = "/{0}/Data/GetRangeValues?startIndex={1}&skip={2}&count={3}&reversed={4}&boundaryType={5}";
        this.updateSingle = "/Data/UpdateValue";
        this.updateMultiple = "/Data/UpdateValues";
        this.removeSingleTemplate = "/{0}/Data/RemoveValue?index={1}";
        this.removeMultipleTemplate = "/{0}/Data/RemoveWindowValues?startIndex={1}&endIndex={2}";
        this.getLast = "/data/getlastvalue";
        this.replaceValue = "/data/replaceValue";
        this.replaceValues = "/data/replaceValues";
        this.tenantId = "localtenant";
        this.token = "";
        this.tokenExpires = "";

        this.getToken = function(authItems){
                                return restCall({
                                                url : authItems["authority"],
                                                method: 'POST',
                                                headers : {
                                                            'Content-Type': 'application/x-www-form-urlencoded'
                                                },
                                                form : {    
                                                            'grant_type' : 'client_credentials',
                                                            'client_id' : authItems['appId'],
                                                            'client_secret' : authItems['appKey'],
                                                            'resource' : authItems['resource']
                                                        }
                                            });
        };

        //parse urls
        this.getLocation = function(location){
            var temp = document.createElement("a");
            temp.href = location;
            return temp.pathname;
        };
		
		//method to create QiNamespaces
		this.createNamespace = function(tenantId, namespace) {
								return restCall({
												url : this.url+this.namespacesBase.format([tenantId]),
												method : 'POST',
												headers : this.getHeaders(),
												body : JSON.stringify(namespace).toString()
											});
		}
		
		//method to delete QiNamespaces
		this.deleteNamespace = function(tenantId, namespaceId) {
								return restCall({
												url : this.url+this.namespacesBase.format([tenantId])+"/"+namespaceId,
												method : 'DELETE',
												headers : this.getHeaders()
											});
		}

        //method to create QiTypes
        this.createType = function(tenantId, namespaceId, wave){
                                return restCall({
                                                url : this.url+this.typesBase.format([tenantId, namespaceId]),
                                                method: 'POST',
                                                headers : this.getHeaders(),
                                                body : JSON.stringify(wave).toString()
                                            });
        };

        //method to get all the Qi types under a tenant Qi Service
        this.getTypes = function(tenantId, namespaceId){
                                return restCall({
                                                url : this.url+this.typesBase.format([tenantId, namespaceId]),
                                                method: 'GET',
                                                headers : this.getHeaders()
                                            });
        };

        //delete a type
        this.deleteType = function(tenantId, namespaceId, typeId){
                                return restCall({
                                            url : this.url+this.typesBase.format([tenantId, namespaceId])+"/"+typeId,
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //create a stream under the Qi Service
        this.createStream = function(tenantId, namespaceId, qiStream){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId]),
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(qiStream).toString()
                                        });
        };

        //get all the streams under the tenant's Qi Service
        this.getStream = function(tenantId, namespaceId, qiStream){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+qiStream.Id,
                                            method : 'GET',
                                            headers : this.getHeaders()
                                        });
        };

        //get all the streams under the tenant's Qi Service
        this.getStreams = function(tenantId, namespaceId){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId]),
                                            method : 'GET',
                                            headers : this.getHeaders()
                                        });
        };

        //update a stream
        this.updateStream = function(tenantId, namespaceId, qiStream){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+qiStream.Id,
                                            method : 'PUT',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(qiStream).toString()
                                        });
        };

        //delete a stream
        this.deleteStream = function(tenantId, namespaceId, streamId){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+streamId,
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //create behavior
        this.createBehavior = function(tenantId, namespaceId, behavior){
                                return restCall({
                                            url : this.url+this.behaviorBase.format([tenantId, namespaceId]),
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(behavior)
                                        });
        };

        //insert an event into a stream
        this.insertEvent = function(tenantId, namespaceId, qiStream, evt){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+
                                                    qiStream.Id+this.insertSingle,
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(evt)
                                        });
        };

        //insert an array of events
        this.insertEvents = function(tenantId, namespaceId, qiStream, events){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+
                                                    qiStream.Id+this.insertMultiple,
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(events)
                                        });
        };

        //update an event
        this.updateEvent = function(tenantId, namespaceId, qiStream, evt){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+
                                                    qiStream.Id+this.updateSingle,
                                            method : 'PUT',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(evt)
                                        });
        };

        //update an array of events
        this.updateEvents = function(tenantId, namespaceId, qiStream, events){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+"/"+
                                                    qiStream.Id+this.updateMultiple,
                                            method : 'PUT',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(events)
                                        });
        };

        //delete an event
        this.deleteEvent = function(tenantId, namespaceId, qiStream, index){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+this.removeSingleTemplate.format([qiStream.Id, index]),
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //delete a window of events
        this.deleteWindowEvents = function(tenantId, namespaceId, qiStream, start, end){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+this.removeMultipleTemplate.format([qiStream.Id, start, end]),
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //retrieve a window of events
        this.getWindowValues = function(tenantId, namespaceId, qiStream, start, end){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+this.getTemplate.format([qiStream.Id,start,end]),
                                            method : 'GET',
                                            headers : this.getHeaders()
                                        });
        };

        //retrieve a range of value based on boundary type
        this.getRangeValues = function(tenantId, namespaceId, qiStream, start, skip, count, reverse, boundaryType){
                                return restCall({
                                            url : this.url+this.streamsBase.format([tenantId, namespaceId])+this.getRangeTemplate.format([qiStream.Id,start,skip,count,reverse,boundaryType]),
                                            method : 'GET',
                                            headers : this.getHeaders()
                                        });
        };

        this.getHeaders = function(){
                                return {
                                            "Authorization" : "bearer "+ this.token,
                                            "Content-type": "application/json", 
                                            "Accept": "text/plain"
                                        }
        };
    }
};