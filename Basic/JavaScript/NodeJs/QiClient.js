

//function to create client object
var qiObjs = require("./QiObjects.js");
var restCall = require("request-promise");

String.prototype.format = function (args) {
    var str = this;
    return str.replace(String.prototype.format.regex, function (item) {
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
    QiClient: function (url) {
        this.url = url;
        this.version = 0.1;
        this.typesBase = "/api/Tenants/{0}/Namespaces/{1}/Types";
        this.streamsBase = "/api/Tenants/{0}/Namespaces/{1}/Streams";
        this.behaviorsBase = "/api/Tenants/{0}/Namespaces/{1}/Behaviors";
        this.insertSingleValueBase = "/Data/InsertValue";
        this.insertMultipleValuesBase = "/Data/InsertValues";
        this.getLastValueBase = "/{0}/Data/GetLastValue";
        this.getWindowValuesBase = "/{0}/Data/GetWindowValues?startIndex={1}&endIndex={2}";
        this.getRangeValuesBase = "/{0}/Data/GetRangeValues?startIndex={1}&skip={2}&count={3}&reversed={4}&boundaryType={5}";
        this.updateSingleValueBase = "/Data/UpdateValue";
        this.updateMultipleValuesBase = "/Data/UpdateValues";
        this.replaceSingleValueBase = "/Data/ReplaceValue";
        this.replaceMultipleValuesBase = "/Data/ReplaceValues";
        this.removeSingleValueBase = "/{0}/Data/RemoveValue?index={1}";
        this.removeMultipleValuesBase = "/{0}/Data/RemoveWindowValues?startIndex={1}&endIndex={2}";
        this.token = "";
        this.tokenExpires = "";

        // returns an access token
        this.getToken = function (authItems) {
            return restCall({
                url: authItems["authority"],
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                form: {
                    'grant_type': 'client_credentials',
                    'client_id': authItems['clientId'],
                    'client_secret': authItems['clientSecret'],
                    'resource': authItems['resource']
                }
            });
        };

        // create a type
        this.createType = function (tenantId, namespaceId, type) {
            return restCall({
                url: this.url + this.typesBase.format([tenantId, namespaceId]),
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(type).toString()
            });
        };

        // create a stream under the Qi Service
        this.createStream = function (tenantId, namespaceId, stream) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]),
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(stream).toString()
            });
        };

        // create behavior
        this.createBehavior = function (tenantId, namespaceId, behavior) {
            return restCall({
                url: this.url + this.behaviorsBase.format([tenantId, namespaceId]),
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(behavior).toString()
            });
        };

        // insert an event into a stream
        this.insertEvent = function (tenantId, namespaceId, streamId, event) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" +
                    streamId + this.insertSingleValueBase,
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(event)
            });
        };

        // insert an array of events
        this.insertEvents = function (tenantId, namespaceId, streamId, events) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" +
                    streamId + this.insertMultipleValuesBase,
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(events)
            });
        };

        // get last value added to stream
        this.getLastValue = function(tenantId, namespaceId, streamId) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.getLastValueBase.format([streamId]),
                method: 'GET',
                headers: this.getHeaders()
            });
        }

        // retrieve a window of events
        this.getWindowValues = function (tenantId, namespaceId, streamId, start, end) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.getWindowValuesBase.format([streamId, start, end]),
                method: 'GET',
                headers: this.getHeaders()
            });
        };

        // retrieve a range of value based on boundary type
        this.getRangeValues = function (tenantId, namespaceId, streamId, start, skip, count, reverse, boundaryType) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.getRangeValuesBase.format([streamId, start, skip, count, reverse, boundaryType]),
                method: 'GET',
                headers: this.getHeaders()
            });
        };

        // update a stream
        this.updateStream = function (tenantId, namespaceId, stream) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" + stream.Id,
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(stream).toString()
            });
        };

        // update an event
        this.updateEvent = function (tenantId, namespaceId, streamId, evt) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" +
                streamId + this.updateSingleValueBase,
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(evt)
            });
        };

        // update an array of events
        this.updateEvents = function (tenantId, namespaceId, streamId, events) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" +
                streamId + this.updateMultipleValuesBase,
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(events)
            });
        };

        // delete an event
        this.deleteEvent = function (tenantId, namespaceId, streamId, index) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.removeSingleValueBase.format([streamId, index]),
                method: 'DELETE',
                headers: this.getHeaders()
            });
        };

        // delete a window of events
        this.deleteWindowEvents = function (tenantId, namespaceId, streamId, start, end) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + this.removeMultipleValuesBase.format([streamId, start, end]),
                method: 'DELETE',
                headers: this.getHeaders()
            });
        };
        
        // delete a type
        this.deleteType = function (tenantId, namespaceId, typeId) {
            return restCall({
                url: this.url + this.typesBase.format([tenantId, namespaceId]) + "/" + typeId,
                method: 'DELETE',
                headers: this.getHeaders()
            });
        };

        // delete a stream
        this.deleteStream = function (tenantId, namespaceId, streamId) {
            return restCall({
                url: this.url + this.streamsBase.format([tenantId, namespaceId]) + "/" + streamId,
                method: 'DELETE',
                headers: this.getHeaders()
            });
        };

        // delete behavior
        this.deleteBehavior = function (tenantId, namespaceId, behaviorId) {
            return restCall({
                url: this.url + this.behaviorsBase.format([tenantId, namespaceId]) + "/" + behaviorId,
                method: 'DELETE',
                headers: this.getHeaders()
            });
        }


        this.getHeaders = function () {
            return {
                "Authorization": "bearer " + this.token,
                "Content-type": "application/json",
                "Accept": "*/*; q=1"
            }
        };
    }
};