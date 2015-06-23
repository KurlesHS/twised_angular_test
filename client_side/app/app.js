(function() {
    angular.module('app', ['ui.router']).controller('MainController', function($scope) {
        $scope.name = 'test name'
    }).
    config(function($stateProvider, $urlRouterProvider) {
            "use strict";
            $urlRouterProvider.otherwise('');
            $stateProvider.state('home', {
                url: '',
                templateUrl: 'templates/home-partial.html'
            }).state('about', {

            });

        });

})();
