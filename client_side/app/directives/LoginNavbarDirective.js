(function () {
    "use strict";
    angular.module('app')
        .directive('loginNavbar', function () {
            "use strict";
            return {
                restrict: 'EA',
                templateUrl: '/templates/login-navbar-dir.html'
            }
        });
})();