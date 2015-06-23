"use strict";

describe('MainController', function () {
    beforeEach(module('app'));
    var $controller;
    beforeEach(inject(function (_$controller_) {
        $controller = _$controller_;
    }));

    it('default name must be equal "test name"', function () {
        var $scope = {};
        var controller = $controller('MainController', {$scope: $scope});
        expect($scope.name).toEqual('test name');
    });
});


describe("suite name", function () {
});