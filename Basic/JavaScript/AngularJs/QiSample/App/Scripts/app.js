'use strict';
angular.module('qisampleApp', ['ngRoute',
                               'ui.bootstrap',
                               'AdalAngular']);


angular.module('qisampleApp')

.constant('QI_SERVER_URL', 'PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL')
.constant('QI_SERVER_APPID', 'PLACEHOLDER_REPLACE_WITH_RESOURCE')
.constant('QI_SAMPLEWEBAPP_CLIENTID', 'PLACEHOLDER_REPLACE_WITH_CLIENTID')



.config(['$routeProvider', '$httpProvider', 'adalAuthenticationServiceProvider', 'QI_SAMPLEWEBAPP_CLIENTID',
    function ($routeProvider, $httpProvider, adalProvider, QI_SAMPLEWEBAPP_CLIENTID) {

    $routeProvider
      .when("/home", {
        controller: "homeCtrl",
        templateUrl: "/App/Views/Home.html",
    }).when("/dashboard", {
        templateUrl: "/App/Views/Dashboard.html",
        requireADLogin: true,
    }).when("/userdata", {
        controller: "userDataCtrl",
        templateUrl: "/App/Views/UserData.html",
    }).otherwise({ redirectTo: "/home" });

    var endpoints = {
        // Map the location of a request to an API to a the identifier of the associated resource
        'PLACEHOLDER_REPLACE_WITH_QI_SERVER_URL': 'PLACEHOLDER_REPLACE_WITH_RESOURCE'
    };


    adalProvider.init(
        {
            instance: 'https://login.microsoftonline.com/',
            clientId: QI_SAMPLEWEBAPP_CLIENTID,
            extraQueryParameter: 'nux=1',
            endpoints: endpoints,
        },
        $httpProvider
        );
   
    }]);
 
