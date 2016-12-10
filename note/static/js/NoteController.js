/**
 * Created by Dmitry on 07/12/2016.
 */
'use strict';

angular.module('noteApp')

    .controller('NoteController', function ($scope, $resource, noteFactory) {

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // create a blank object to handle form data.
        $scope.userdata = {};
        
        $scope.notes = {};
        
        $scope.getNotes = function () {
            return noteFactory.query();
        };
        $scope.submitForm = function () {
            // Posting data
            var csrf = getCookie('csrftoken');
            var config = {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded;',
                    'X-CSRFToken': csrf
                }
            };
            $http.post('', $scope.userdata, config)
                .then(
                    function (response) {

                    }
                )
        };

        angular.element(document).ready(function () {
            $scope.notes = noteFactory.getNotes().query(
                function (response) {
                    $scope.notes = response;
                    $scope.showNotes = true;
                }
            );
        });
    });