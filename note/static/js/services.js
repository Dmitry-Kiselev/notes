/**
 * Created by Dmitry on 07/12/2016.
 */
'use strict';

angular.module('noteApp')
    .constant("baseURL", "/")
    .service('noteFactory', ['$resource', 'baseURL', function ($resource, baseURL) {

        this.getNotes = function () {
            return $resource(baseURL + "notes/:id", null, {'update': {method: 'PUT'}});
        };
        this.getLabels = function () {
            return $resource(baseURL + "labels/:id", null, {'update': {method: 'PUT'}});
        };
        this.getCategories = function () {
            return $resource(baseURL + "categories/:id", null, {'update': {method: 'PUT'}});
        }
    }]);
