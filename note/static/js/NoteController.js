/**
 * Created by Dmitry on 07/12/2016.
 */
'use strict';

angular.module('noteApp')

    .controller('NoteController', function ($scope, $resource, noteFactory) {

        var DEFAULT_COLOR = "blue-grey darken-1";

        // create a blank object to handle form data.
        $scope.userdata = {};
        $scope.notes = [];
        $scope.curNote = {};


        angular.element(document).ready(function () {
            // Initialize collapse button
            $("#sidenav-btn").sideNav();
            // Initialize collapsible (uncomment the line below if you use the dropdown variation)
            $('#noteModal').modal();
            $('select').material_select();
            $scope.notes = noteFactory.notesManager().query(
                function () {
                    $scope.showNotes = true;
                }
            );
            $scope.labels = noteFactory.labelsManager().query(
                function () {
                    $scope.showLabels = true;

                }
            );
            $scope.categories = noteFactory.categoriesManager().query(
                function () {
                    $scope.showCategories = true;
                }
            );

            $scope.activateSelect = function () {
                $('select').material_select();
            };

            $scope.sendNote = function () {
                if ($scope.curNote.id) {
                    noteFactory.notesManager().update({id: $scope.curNote.id}, $scope.curNote);
                    $scope.notes[$scope.curNote.id] = $scope.curNote;
                    $scope.curNote = {}
                }
                else {
                    noteFactory.notesManager().save($scope.curNote);
                    $scope.curNote.color = DEFAULT_COLOR;
                    $scope.notes.push($scope.curNote);
                    $scope.curNote = {}
                }
                $scope.curNote = {};
            };

            $scope.deleteNote = function (id) {
                noteFactory.notesManager().delete({id: id});
                var index = $scope.notes.findIndex(x = > x.id == id);
                $scope.notes.pop(index);
            };
        });
    });
