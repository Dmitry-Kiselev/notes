/**
 * Created by Dmitry on 07/12/2016.
 */
'use strict';

angular.module('noteApp')

.controller('NoteController', function($scope, $resource, noteFactory, Upload, $timeout) {

    var DEFAULT_COLOR = "blue-grey darken-1";

    $scope.colors = [{
        'color': 'red',
        'class': 'red darken-1'
    }, {
        'color': 'purple',
        'class': 'purple darken-1'
    }, {
        'color': 'amber',
        'class': 'amber accent-1'
    }, {
        'color': 'cyan',
        'class': 'cyan darken-1'
    }, {
        'color': 'grey',
        'class': 'blue-grey darken-1'
    }, {
        'color': 'indigo',
        'class': 'indigo darken-1'
    }, {
        'color': 'light green',
        'class': 'light-green darken-1'
    }, {
        'color': 'pink',
        'class': 'pink darken-1'
    }];

    // create a blank object to handle form data.
    $scope.userdata = {};
    $scope.notes = [];
    $scope.curNote = {};
    $scope.curLabel = {};


    angular.element(document).ready(function() {
        // Initialize collapse button
        $("#sidenav-btn").sideNav();
        // Initialize collapsible (uncomment the line below if you use the dropdown variation)
        $('#noteModal').modal();
        $('#labelModal').modal();
        $('select').material_select();
        $scope.notes = noteFactory.notesManager().query(
            function() {
                $scope.showNotes = true;
            }
        );
        $scope.labels = noteFactory.labelsManager().query(
            function() {
                $scope.showLabels = true;

            }
        );
        $scope.categories = noteFactory.categoriesManager().query(
            function() {
                $scope.showCategories = true;
            }
        );

        $scope.activateSelect = function() {
            $('select').material_select();
        };

        $scope.sendNote = function() {
            if ($scope.curNote.id) {
                noteFactory.notesManager().update({
                    id: $scope.curNote.id
                }, $scope.curNote);
                var index = $scope.notes.findIndex(x => x.id == $scope.curNote.id);
                $scope.notes[index] = $scope.curNote;
                $scope.curNote = {};
            } else {
                noteFactory.notesManager().save($scope.curNote);
                if (!$scope.curNote.color && !$scope.curNote.id) {
                    $scope.curNote.color = DEFAULT_COLOR;
                }
                $scope.notes.push($scope.curNote);
                $scope.curNote = {}
            }
            $scope.curNote = {};
        };

        $scope.deleteNote = function(id) {
            noteFactory.notesManager().delete({
                id: id
            });
            var index = $scope.notes.findIndex(x => x.id == id);
            $scope.notes.pop(index);
        };


        $scope.editNote = function(id) {
            var index = $scope.notes.findIndex(x => x.id == id);
            $scope.curNote = $scope.notes[index];
            $('#noteModal').modal('open');
        };

        $scope.checkSelected = function() {
            try {
                $('#label_select').val($scope.curNote.labels).trigger('update');
                $('#label_select').material_select();
            } catch (err) {
                // do nothing
            }
        };

        $scope.sendLabel = function() {
            if ($scope.curLabel.id) {
                noteFactory.labelsManager().update({
                    id: $scope.curLabel.id
                }, $scope.curLabel);
                var index = $scope.labels.findIndex(x => x.id == $scope.curLabel.id);
                $scope.labels[index] = $scope.curLabel;
                $scope.curLabel = {};
            } else {
                noteFactory.labelsManager().save($scope.curLabel);
                $scope.labels.push($scope.curLabel);
                $scope.curLabel = {}
            }
            $scope.curLabel = {};
        };

    });
});