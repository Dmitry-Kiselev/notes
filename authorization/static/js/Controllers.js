'use strict';

angular.module('authApp')

    .controller('UserDataController', function ($scope, $http, $window) {

        // create a blank object to handle form data.
        $scope.userdata = {};
        $scope.submitForm = function () {
            // Posting data
            $http.post('', $scope.userdata)
                .then(
                    function (response) {
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
    })

    .controller('PasswordResetController', function ($scope, $http, $window) {

        $scope.userdata = {};

        $scope.submitEmail = function () {
            $http.post('', $scope.userdata).then(
                function (response) {
                    if (response.data.has_error) {
                        $scope.userdata.errors = response.data.errors;
                        // Materialize.toast(message, displayLength, className, completeCallback);
                        Materialize.toast($scope.userdata.errors, 10000); // 10000 is the duration of the toast
                    }
                    else {
                        $('#content').html(response.data);
                    }
                }
            );
        };

        $scope.passwordSubmit = function () {
            $http.post('', $scope.userdata).then(
                function (response) {
                    if (response.data.has_error) {
                        $scope.userdata.errors = response.data.errors;

                        for (var error in $scope.userdata.errors) {
                            // Materialize.toast(message, displayLength, className, completeCallback);
                            Materialize.toast($scope.userdata.errors[error], 10000); // 10000 is the duration of the toast
                        }
                    }
                    else {
                        $('#content').html(response.data);
                    }
                }
            );
        }

    })
;
