(function(){
    "use strict";
    angular.module('app')
        .controller('LoginController', function($scope) {
            $scope.name = '';
            $scope.password = '';
            $scope.isAuthorized = false;
            $scope.login = function() {
                console.log('try to login with login ', $scope.name, 'and password ', $scope.password);
                $scope.isAuthorized = true;

            };
            $scope.logout = function() {
                console.log('try to logout');
                $scope.isAuthorized = false;
                $scope.$apply()
            };

        })
})();