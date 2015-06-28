(function () {
    "use strict";
    angular.module('app')
        .factory('LoginService', ['CredentialService', '$http', function (CredentialService, $http) {
            var isAuthorized = false;
            var listeners = [];
            var name = '';
            var password = '';
           // console.log('init login service', sessionStorage.getItem('token'), 'http provider', $httpProvider);
            var token = sessionStorage.getItem('token');

            var setAuthorized = function (auth) {
                if (isAuthorized != auth) {
                    isAuthorized = auth;
                    listeners.forEach(function (callback) {
                        callback(auth);
                    });
                }
            };
            var addListener = function (listener) {
                listeners.push(listener);
            };

            var login = function (name, password) {
                this.name = name;
                CredentialService.userName = name;
                CredentialService.userPassword = password;
                this.password = password;

                $http.post('/api/1.0/login', {userName: name})
                    .success(function (data, status, headers, config) {
                        console.log('success', data, status, headers, config);
                        var token = data['token'];
                        CredentialService.token = token;
                        sessionStorage.setItem('token', token);
                        $http.get('/api/1.0/login')
                            .success(function(data, status, headers, config) {
                                setAuthorized(true)
                            })
                            .error(function(data, status, headers, config) {
                                $.notify('error with credentials', 'info');
                            });
                    })
                    .error(function (data, status, headers, config) {
                        console.log('error', data, status, headers, config);
                        $.notify('error with credentials', 'info');
                    });
            };

            var logout = function () {
                setAuthorized(false);
            };

            return {
                name: name,
                password: password,
                addListener: addListener,
                setAuthorized: setAuthorized,
                login: login,
                logout: logout
            };
        }]);
})();