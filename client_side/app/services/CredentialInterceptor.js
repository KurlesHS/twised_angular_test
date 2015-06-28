(function () {
    "use strict";
    angular.module('app')
        .factory('CredentialInterceptor', ['CredentialService', 'md5', function (CredentialService, md5) {
            console.log('cred inter factory');
            return {
                'request': function (config) {
                    console.log('http intercept');
                    if (CredentialService.token) {
                        var number = CredentialService.currentNumber++;
                        var strToMd5 = [CredentialService.token, CredentialService.userPassword, number].join('.');
                        var strMd5 = md5.createHash(strToMd5);
                        console.log('http inject, hash of ' + strToMd5 + ' is ' + strMd5);
                        config.headers['x-session-token'] = [CredentialService.token, strMd5, number].join('.');
                    }
                    return config;
                }
            };
        }])

        .config(['$httpProvider', function ($httpProvider) {
            $httpProvider.interceptors.push('CredentialInterceptor');
        }])

    ;
})();