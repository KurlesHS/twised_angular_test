(function() {
    "use strict";
    angular.module('app')
        .factory('CredentialService', [function() {
            var userName = '';
            var userPassword = '';
            var token = null;
            var currentNumber = 0;
            return {
                userName: userName,
                userPassword: userPassword,
                token: token,
                currentNumber: currentNumber
            }
        }]);
})();