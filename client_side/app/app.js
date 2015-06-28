(function() {
    "use strict";
    angular.module('app', ['ui.router', 'angular-md5']).controller('MainController', function($scope) {

    }).
    config(function($stateProvider, $urlRouterProvider) {
            "use strict";
            $urlRouterProvider.otherwise('');
            $stateProvider.state('home', {
                url: '',
                views: {
                    '' : {templateUrl: 'templates/home-partial.html'}
                }
            }).state('about', {

            });

        });

})();
