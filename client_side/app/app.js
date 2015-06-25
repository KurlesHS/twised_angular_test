(function() {
    angular.module('app', ['ui.router',]).controller('MainController', function($scope) {
        $scope.name = ''

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
