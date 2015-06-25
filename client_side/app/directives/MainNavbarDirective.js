(function () {
    angular.module('app')
        .directive('mainNavbar', function () {
            "use strict";
            return {
                restrict: 'EA',
                templateUrl: '/templates/main-navbar-dir.html'
            }
        });
})();