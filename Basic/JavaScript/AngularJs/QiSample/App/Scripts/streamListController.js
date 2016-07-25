'use strict';
angular.module('qisampleApp')
    .controller('streamListController', ['$scope', '$location', '$interval', 'QiService', 'adalAuthenticationService',
        function ($scope, $location, $interval, QiService, adalService) {
        $scope.error = "";
        $scope.loadingMessage = "Loading...";
        $scope.streamList = null;
        $scope.editingInProgress = false;
        $scope.newToGoCaption = "";
        $scope.pollingInterval = 3000;
        var tenantId = "a5e7fb7a-48c8-4a4d-8ef4-0a7ad0abdc19";
        var namespaceId = "VizSamples";

        var _selectedStreams = [];
        $scope.isStreamSelected = function (streamId) {
            for (var i = 0; i < _selectedStreams.length; i++) {
                if (_selectedStreams[i].Id == streamId) {
                    return true;
                }
            }
            return false;
        };
        $scope.selectInsertStream = function (stream) {
            var addedToExistingItem = false;
            for (var i = 0; i < _selectedStreams.length; i++) {
                if (_selectedStreams[i].Id == stream.Id) {
                    _selectedStreams[i].count++;
                    addedToExistingItem = true;
                    break;
                }
            }
            if (!addedToExistingItem) {
                _selectedStreams.push({
                    count: 1, Id: stream.Id, desc: stream.description
                });
            }
        };
        $scope.selectRemoveStream = function (stream) {
            for (var i = 0; i < _selectedStreams.length; i++) {
                if (_selectedStreams[i].Id == stream.Id) {
                    _selectedStreams.splice(i, 1);
                    break;
                }
            }
        };
        $scope.populateQiStreams = function () {
            QiService.getStreams(tenantId, namespaceId).then(function (res1) {
                $scope.streamList = res1.data;
            });
        };
        $scope.selectedDataList = function () {
            return _selectedStreams;
        };
        $scope.isDataListPopulated = function () {
            return _selectedStreams.length > 0;
        };
        var _dataList = [];
        $interval(function () {
            _selectedStreams.forEach(function (item) {
                QiService.getLastValue(tenantId, namespaceId, item.Id)
                    .then(function (results) {
                    var data = results.data;
                    $scope.insertToDataList(item.Id, data);
                });
            });
        }, $scope.pollingInterval);
        $scope.insertToDataList = function (Id, entry) {
            var addedToExistingDataItem = false;
            for (var i = 0; i < _dataList.length; i++) {
                if (_dataList[i].Id == Id) {
                    _dataList[i].Timestamp = entry.Timestamp;
                    _dataList[i].Temperature = entry.Temperature;
                    _dataList[i].Pressure = entry.Pressure;
                    _dataList[i].Depth = entry.Depth;
                    addedToExistingDataItem = true;
                    break;
                }
            }
            if (!addedToExistingDataItem) {
                _dataList.push({
                    count: 1, Id: Id, Timestamp: entry.Timestamp,
                    Temperature: entry.Temperature,
                    Pressure: entry.Pressure,
                    Depth: entry.Depth
                });
            }
        };
        $scope.getTimeStamp = function (Id) {
            for (var i = 0; i < _dataList.length; i++) {
                if (_dataList[i].Id == Id) {
                    return _dataList[i].Timestamp;
                }
            }
            return null;
        };
        $scope.getTemperature = function (Id) {
            for (var i = 0; i < _dataList.length; i++) {
                if (_dataList[i].Id == Id) {
                    return _dataList[i].Temperature;
                }
            }
            return null;
        };
        $scope.getPressure = function (Id) {
            for (var i = 0; i < _dataList.length; i++) {
                if (_dataList[i].Id == Id) {
                    return _dataList[i].Pressure;
                }
            }
            return null;
        };
        $scope.getDepth = function (Id) {
            for (var i = 0; i < _dataList.length; i++) {
                if (_dataList[i].Id == Id) {
                    return _dataList[i].Depth;
                }
            }
            return null;
        };
        
    }]);
//# sourceMappingURL=streamListController.js.map