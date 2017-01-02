/**
 * Created by Dmitry on 07/12/2016.
 */
'use strict';

angular.module('noteApp')
    .constant("baseURL", "/")
    .service('noteFactory', ['$resource', 'baseURL', function ($resource, baseURL) {

        this.notesManager = function () {
            return $resource(baseURL + "notes/:id", null, {'update': {method: 'PUT'}});
        };
        this.labelsManager = function () {
            return $resource(baseURL + "labels/:id", null, {'update': {method: 'PUT'}});
        };
        this.categoriesManager = function () {
            return $resource(baseURL + "categories/:id", null, {'update': {method: 'PUT'}});
        };
        this.userManager = function () {
            return $resource(baseURL + "users/:id", null, {'update': {method: 'PUT'}});
        };
        this.imagesManager = function () {
            return $resource(baseURL + "images/:id", null, {'update': {method: 'PUT'}});
        };
        this.filesManager = function () {
            return $resource(baseURL + "files/:id", null, {'update': {method: 'PUT'}});
        };
    }]);
