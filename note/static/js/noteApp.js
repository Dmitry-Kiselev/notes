/**
 * Created by Dmitry on 07/12/2016.
 */
'use strict';

var app = angular.module("noteApp", ['ngResource']);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

app.config(function ($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
