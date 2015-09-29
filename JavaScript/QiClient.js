

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
        this.typesBase = "/Qi/Types";
        this.streamsBase = "/Qi/Streams";
        this.behaviorBase = "/Qi/Behaviors";
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

        //method to create QiTypes
        this.createType = function(wave){
                                return restCall({
                                                url : this.url+this.typesBase,
                                                method: 'POST',
                                                headers : this.getHeaders(),
                                                body : JSON.stringify(wave).toString()
                                            });
        };

        //method to get all the Qi types under a tenant Qi Service
        this.getTypes = function(){
                                return restCall({
                                                url : this.url+this.typesBase,
                                                method: 'GET',
                                                headers : this.getHeaders()
                                            });
        };

        //delete a type
        this.deleteType = function(typeId){
                                return restCall({
                                            url : this.url+this.typesBase+"/"+typeId,
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //create a stream under the Qi Service
        this.createStream = function(qiStream){
                                return restCall({
                                            url : this.url+this.streamsBase,
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(qiStream).toString()
                                        });
        };

        //get all the streams under the tenant's Qi Service
        this.getStream = function(qiStream){
                                return restCall({
                                            url : this.url+this.streamsBase+"/"+qiStream.Id,
                                            method : 'GET',
                                            headers : this.getHeaders()
                                        });
        };

        //get all the streams under the tenant's Qi Service
        this.getStreams = function(){
                                return restCall({
                                            url : this.url+this.streamsBase,
                                            method : 'GET',
                                            headers : this.getHeaders()
                                        });
        };

        //update a stream
        this.updateStream = function(qiStream){
                                return restCall({
                                            url : this.url+this.streamsBase+"/"+qiStream.Id,
                                            method : 'PUT',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(qiStream).toString()
                                        });
        };

        //delete a stream
        this.deleteStream = function(streamId){
                                return restCall({
                                            url : this.url+this.streamsBase+"/"+streamId,
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //create behavior
        this.createBehavior = function(behavior){
                                return restCall({
                                            url : this.url+this.behaviorBase,
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(behavior)
                                        });
        };

        //insert an event into a stream
        this.insertEvent = function(qiStream, evt){
                                return restCall({
                                            url : this.url+this.streamsBase+"/"+
                                                    qiStream.Id+this.insertSingle,
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(evt)
                                        });
        };

        //insert an array of events
        this.insertEvents = function(qiStream, events){
                                return restCall({
                                            url : this.url+this.streamsBase+"/"+
                                                    qiStream.Id+this.insertMultiple,
                                            method : 'POST',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(events)
                                        });
        };

        //update an event
        this.updateEvent = function(qiStream, evt){
                                return restCall({
                                            url : this.url+this.streamsBase+"/"+
                                                    qiStream.Id+this.updateSingle,
                                            method : 'PUT',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(evt)
                                        });
        };

        //update an array of events
        this.updateEvents = function(qiStream, events){
                                return restCall({
                                            url : this.url+this.streamsBase+"/"+
                                                    qiStream.Id+this.updateMultiple,
                                            method : 'PUT',
                                            headers : this.getHeaders(),
                                            body : JSON.stringify(events)
                                        });
        };

        //delete an event
        this.deleteEvent = function(qiStream, index){
                                return restCall({
                                            url : this.url+this.streamsBase+this.removeSingleTemplate.format([qiStream.Id, index]),
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //delete a window of events
        this.deleteWindowEvents = function(qiStream, start, end){
                                return restCall({
                                            url : this.url+this.streamsBase+this.removeMultipleTemplate.format([qiStream.Id, start, end]),
                                            method : 'DELETE',
                                            headers : this.getHeaders()
                                        });
        };

        //retrieve a window of events
        this.getWindowValues = function(qiStream, start, end){
                                return restCall({
                                            url : this.url+this.streamsBase+this.getTemplate.format([qiStream.Id,start,end]),
                                            method : 'GET',
                                            headers : this.getHeaders()
                                        });
        };

        //retrieve a range of value based on boundary type
        this.getRangeValues = function(qiStream, start, skip, count, reverse, boundaryType){
                                return restCall({
                                            url : this.url+this.streamsBase+this.getRangeTemplate.format([qiStream.Id,start,skip,count,reverse,boundaryType]),
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