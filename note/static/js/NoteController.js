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
        $('.modal').modal();
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

        $scope.users = noteFactory.userManager().query(
            function() {
                $scope.showUsers = true;
                $scope.userObj = {};
                for (var i in $scope.users) {
                    $scope.userObj[$scope.users[i]] = null;
                }
                $('input.autocomplete').autocomplete({
                    data: $scope.userObj
                });
            }
        );

        $scope.activateSelect = function() {
            $('select').material_select();
        };

        $scope.sendNote = function() {
            if ($scope.curNote.id) {
                noteFactory.notesManager().update({
                    id: $scope.curNote.id
                }, $scope.curNote, function(response) {
                    var index = $scope.notes.findIndex(x => x.id == $scope.curNote.id);
                    $scope.notes[index] = response;
                });
                var index = $scope.notes.findIndex(x => x.id == $scope.curNote.id);
                $scope.notes[index] = $scope.curNote;
            } else {
                noteFactory.notesManager().save($scope.curNote, function(response) {
                    $scope.notes.push(response);
                    $scope.curNote = response;
                });
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
            var labels = [];
            /* we need to do this, because in select statement angular compares entire objects
            and even if they have same properties they do not match*/
            for (var l in $scope.curNote.labels) {
                for (var i in $scope.labels) {
                    if ($scope.curNote.labels[l].id == $scope.labels[i].id) {
                        labels.push($scope.labels[i])
                    }
                }
            }
            $scope.curNote.labels = labels;
            $('#noteModal').modal('open');
        };

        $scope.sendLabel = function() {
            if ($scope.curLabel.id) {
                noteFactory.labelsManager().update({
                    id: $scope.curLabel.id
                }, $scope.curLabel);
                var index = $scope.labels.findIndex(x => x.id == $scope.curLabel.id);
                $scope.labels[index] = $scope.curLabel;
            } else {
                noteFactory.labelsManager().save($scope.curLabel);
                $scope.labels.push($scope.curLabel);
            }
            $scope.curLabel = {};
        };

        // for multiple images:
        $scope.uploadImages = function(files) {
            var clear = true;
            if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                    Upload.upload({
                        data: {
                            image: files[i]
                        },
                        url: '/images/',
                        method: 'POST'
                    }).then(function(response) {
                        if (clear) {
                            $scope.curNote.images = [];
                            clear = false;
                        }
                        $scope.curNote.images.push(response.data);
                    });
                }
            }
        };

        // for multiple files upload:
        $scope.uploadFiles = function(files) {
            var clear = true;
            if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                    Upload.upload({
                        data: {
                            file: files[i]
                        },
                        url: '/files/',
                        method: 'POST'
                    }).then(function(response) {
                        if (clear) {
                            $scope.curNote.files = [];
                            clear = false;
                        }
                        $scope.curNote.files.push(response.data);
                    });
                }
            }
        };

        $scope.setFilter = function(name) {
            $scope.searchText = name;
        };

        $scope.noteDetail = function(id) {
            var index = $scope.notes.findIndex(x => x.id == id);
            $scope.curNote = $scope.notes[index];
            $('#detailModal').modal();
        };

        $scope.clearCurNote = function() {
            $scope.curNote = {};
        };

        $scope.shareNote = function(id) {
            $scope.shareObj = {
                'note': id
            };
            $('#shareModal').modal('open');
        };

        $scope.sendSharedWith = function() {
            if ($scope.shareObj.user && $scope.shareObj.note) {
                noteFactory.userManager().update($scope.shareObj);
            }
        }
    });
});