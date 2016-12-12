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
        $scope.notes = [];
        $scope.curNote = {};

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
            // Initialize collapse button
            $("#sidenav-btn").sideNav();
            // Initialize collapsible (uncomment the line below if you use the dropdown variation)
            $('#noteModal').modal();
            $('select').material_select();
            $scope.getNotes = noteFactory.getNotes().query(
                function (response) {
                    $scope.notes = response;
                    $scope.showNotes = true;
                }
            );
            $scope.getLabels = noteFactory.getLabels().query(
                function (response) {
                    $scope.labels = response;
                    $scope.showLabels = true;

                }
            );
            $scope.getCategories = noteFactory.getCategories().query(
                function (response) {
                    $scope.categories = response;
                    $scope.showCategories = true;
                }
            );

            $scope.activateSelect = function () {
                $('select').material_select();
            };
        });
    });


angular.module('noteApp').filter('cut', function () {
    return function (value, wordwise, max, tail) {
        if (!value) return '';

        max = parseInt(max, 10);
        if (!max) return value;
        if (value.length <= max) return value;

        value = value.substr(0, max);
        if (wordwise) {
            var lastspace = value.lastIndexOf(' ');
            if (lastspace != -1) {
                //Also remove . and , so its gives a cleaner result.
                if (value.charAt(lastspace - 1) == '.' || value.charAt(lastspace - 1) == ',') {
                    lastspace = lastspace - 1;
                }
                value = value.substr(0, lastspace);
            }
        }

        return value + (tail || ' …');
    };
});
