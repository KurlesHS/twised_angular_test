(function () {
    "use strict";
    angular.module('app')
        .controller('LoginController', ["$scope", "LoginService", function ($scope, LoginService) {
            $scope.loginService = LoginService;
            $scope.name = LoginService.name;
            $scope.password = LoginService.password;

            $scope.setAuthorized = function(auth) {
                console.log('set auth in controller:', auth);
               $scope.isAuthorized = auth;
            };
            LoginService.addListener($scope.setAuthorized);

            $scope.logout = function () {
                console.log('try to logout');
                LoginService.logout();
            };

            $scope.login = function () {
                console.log('try to login');
                LoginService.login($scope.name, $scope.password);
            };
        }]);
})();