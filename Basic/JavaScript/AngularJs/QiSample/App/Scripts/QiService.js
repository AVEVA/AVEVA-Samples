angular.module('qisampleApp')
    .factory('QiService', ['$http', '$q', 'QI_SERVER_URL', function ($http, $q, QI_SERVER_URL) {
        var qiServerUrl = QI_SERVER_URL;
        var url = qiServerUrl;
        var tenantsBase = "/Qi/Tenants";
        var namespacesBase = "/Qi/{0}/Namespaces";
        var typesBase = "/Qi/{0}/{1}/Types";
        var streamsBase = "/Qi/{0}/{1}/Streams";
        var behaviorBase = "/Qi/{0}/{1}/Behaviors";
        var insertSingle = "/Data/InsertValue";
        var insertMultiple = "/Data/InsertValues";
        var getTemplate = "/{0}/Data/GetWindowValues?startIndex={1}&endIndex={2}";
        var getRangeTemplate = "/{0}/Data/GetRangeValues?startIndex={1}&count={2}";
        
                
        return {
            getNamespaces: function (tenantId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/Namespaces";
                $http({
                    url: myurl,
                    method: 'GET',
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

            //get all the streams under the tenant's Qi Service
            getStreams: function (tenantId, namespaceId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + namespaceId + "/Streams";
                $http({
                    url: myurl,
                    method: 'GET',
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },
            
            getLastValue: function (tenantId, namespaceId, qiStream, start, count) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + namespaceId + "/Streams" + "/" + qiStream + "/Data/GetLastValue";
                $http({
                    url: myurl,
                    method: 'GET',
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

            getOrCreateNameSpace: function (tenantId, namespaceId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/Namespaces";
                $http({
                    url: myurl,
                    method: 'POST',
                    data: JSON.stringify(namespaceId).toString(),
                    headers: {'Content-Type': 'application/json'}
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

            getNamespace: function (tenantId, namespaceId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/Namespaces/" +namespaceId;
                $http({
                    url: myurl,
                    method: 'GET',
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },
    
            getType: function (tenantId, nameSpaceId, typeId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Types/" + typeId;
                $http({
                    url: myurl,
                    method: 'GET',
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

            getTypes: function (tenantId, nameSpaceId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Types/";
                $http({
                    url: myurl,
                    method: 'GET',
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

             getorCreateTypes: function (tenantId, nameSpaceId, type) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Types/";
                $http({
                    url: myurl,
                    method: 'POST',
                    data: JSON.stringify(type).toString(),
                    headers: { 'Content-Type': 'application/json' }
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

            deleteType: function (tenantId, nameSpaceId, typeId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Types/" + typeId;
                $http({
                    url: myurl,
                    method: 'DELETE',
                    data: { Id: typeId }
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

            updateType: function (tenantId, nameSpaceId, typeId) {
                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Types/" + typeId;
                $http({
                    url: myurl,
                    method: 'DELETE',
                    data: { Id: typeId }
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

            createStream: function(tenantId, nameSpaceId, qiStream){

                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams";
                $http({
                    url: myurl,
                    method: 'POST',
                    data: JSON.stringify(qiStream).toString()
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
            },

        //get all the streams under the tenant's Qi Service
            getStream: function (tenantId, namespaceId, qiStreamId) {

                var deferred = $q.defer();
                var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId;
                $http({
                    url: myurl,
                    method: 'GET'
                }).then(function (response) {
                    deferred.resolve(response);
                }, function (error) {
                    deferred.reject(error);
                });
                return deferred.promise;
        },

   

        //update a stream
            updateStream: function (tenantId, nameSpaceId, qiStream) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/"+ qiStream.Id;
            $http({
                url: myurl,
                method: 'PUT',
                data: JSON.stringify(qiStream).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //delete a stream
            deleteStream: function (tenantId, nameSpaceId, streamId) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + streamId;
            $http({
                url: myurl,
                method: 'DELETE'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },



        //insert an event into a stream
        insertValue: function (tenantId, nameSpaceId, qiStreamId, evt) {

            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId+ "/Data/InsertValue";
            $http({
                url: myurl,
                method: 'POST',
                data: JSON.stringify(evt).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //insert an array of events
        insertValues: function (tenantId, nameSpaceId, qiStreamId, events) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/InsertValues";
            $http({
                url: myurl,
                method: 'POST',
                data: JSON.stringify(events).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //update an event
        updateValue: function (tenantId, nameSpaceId, qiStreamId, evt) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/UpdateValue";
            $http({
                url: myurl,
                method: 'PUT',
                data: JSON.stringify(evt).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //update an array of events
        updateValues: function (tenantId, nameSpaceId, qiStreamId, events) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/UpdateValues";
            $http({
                url: myurl,
                method: 'PUT',
                data: JSON.stringify(events).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //delete an event
        removeValue: function (tenantId, nameSpaceId, qiStreamId, index) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/RemoveValue?index=" + index;
            $http({
                url: myurl,
                method: 'DELETE'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //delete a window of events
        removeWindowValues: function (tenantId, nameSpaceId, qiStreamId, start, end) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/RemoveWindowValues?startIndex="
                + start + "&endIndex=" + end;
            $http({
                url: myurl,
                method: 'DELETE'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //retrieve a window of events
        getWindowValues: function (tenantId, nameSpaceId, qiStreamId, start, end) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/GetWindowValues?startIndex="
                + start + "&endIndex=" + end;
            $http({
                url: myurl,
                method: 'GET'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //retrieve a range of value based on boundary type
        getRangeValues: function (tenantId, nameSpaceId, qiStreamId, start, skip, count, reverse, boundaryType) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Streams/" + qiStreamId + "/Data/GetRangeValues?startIndex="
                + start + "&skip=" + skip + "&count=" + count + "&reversed=" + reverse + "&boundaryType=" + boundaryType;
            $http({
                url: myurl,
                method: 'GET'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
        },

        //create behavior
        createBehavior: function (tenantId, nameSpaceId, behavior) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Behaviors";
            $http({
                url: myurl,
                method: 'POST',
                data: JSON.stringify(behavior).toString()
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;
            
        },

        deleteBehavior: function (tenantId, nameSpaceId, behaviorId) {
            var deferred = $q.defer();
            var myurl = url + "/Qi/" + tenantId + "/" + nameSpaceId + "/Behaviors/" + behaviorId;
            $http({
                url: myurl,
                method: 'DELETE'
            }).then(function (response) {
                deferred.resolve(response);
            }, function (error) {
                deferred.reject(error);
            });
            return deferred.promise;

        },

        };
    }]);
