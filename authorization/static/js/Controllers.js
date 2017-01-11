'use strict';

angular.module('authApp')

    .controller('UserDataController', function ($scope, $http, $window) {

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
                        //redirecting or something else
                        $scope.userdata = {};  // to choose correct action in view
                        // after registration to provide friendly login
                        if (response.data.has_error) {
                            $scope.userdata.errors = response.data.errors;

                            for (var error in $scope.userdata.errors) {
                                // Materialize.toast(message, displayLength, className, completeCallback);
                                Materialize.toast($scope.userdata.errors[error], 10000); // 10000 is the duration of the toast
                            }
                        }
                        else {
                            $window.location = '/';
                        }
                        $scope.userdata.response = response.data.response;
                    }
                )
        };

        angular.element(document).ready(function () {
            angular.element('#authModal').modal({dismissible: false});
            angular.element('#authModal').modal('open');
            $('ul.tabs').tabs();
        });
    });
