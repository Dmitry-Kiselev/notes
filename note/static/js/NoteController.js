/**
 * Created by Dmitry on 07/12/2016.
 */
'use strict';

angular.module('noteApp')

.controller('NoteController', function($scope, $resource, noteFactory, Upload) {


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
    $scope.shareFlag = false;


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
            var categories = [];
            /* we need to do this, because in select statement angular compares entire objects
            and even if they have same properties they do not match*/
            for (var l in $scope.curNote.labels) {
                for (var i in $scope.labels) {
                    if ($scope.curNote.labels[l].id == $scope.labels[i].id) {
                        labels.push($scope.labels[i])
                    }
                }
            }
            for (var l in $scope.curNote.categories) {
                for (var i in $scope.categories) {
                    if ($scope.curNote.categories[l].id == $scope.categories[i].id) {
                        categories.push($scope.categories[i])
                    }
                }
            }
            $scope.curNote.labels = labels;
            $scope.curNote.categories = categories;
            $('#noteModal').modal('open');
        };

        $scope.sendLabel = function() {
            if ($scope.curLabel.id) {
                noteFactory.labelsManager().update({
                    id: $scope.curLabel.id
                }, $scope.curLabel, function(response) {
                    var index = $scope.labels.findIndex(x => x.id == $scope.curLabel.id);
                    $scope.labels[index] = response;
                });
            } else {
                noteFactory.labelsManager().save($scope.curLabel, function(response) {
                    $scope.labels.push(response);
                });
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
                var index = $scope.notes.findIndex(x => x.id == $scope.shareObj.note);
                $scope.notes[index].shared_with.push($scope.users.indexOf($scope.shareObj.user) + 1);
            }
        };

        $scope.filterFn = function(item) {
            // must have array, and array must be empty
            if (item.shared_with && item.shared_with.length != 0) {
                $scope.shareFlag = true;
                return true;
            }
        };

        $scope.deleteShare = function(note_id, user_id) {
            var note_index = $scope.notes.findIndex(x => x.id == note_id);
            var index = $scope.notes[note_index].shared_with.indexOf(user_id);
            if (index >= 0) {
                $scope.notes[note_index].shared_with.splice(index, 1);
            }
            var shareRelation = {
                'note': note_id,
                'user': user_id
            };
            noteFactory.userManager().delete(shareRelation);
        };

        $scope.deleteCategoriesAndLabels = function(type, id) {
            var manager = null;
            if (type == 'label') {
                manager = noteFactory.labelsManager();
                var index = $scope.labels.findIndex(x => x.id == id);
                $scope.labels.pop(index);
            }
            if (type == 'category') {
                manager = noteFactory.categoriesManager();
                var index = $scope.categories.findIndex(x => x.id == id);
                $scope.categories.pop(index);
            }
            manager.delete({
                id: id
            });
        };

        $scope.makeCategoryTree = function(parent_id) {

            if (!parent_id) {
                return "";
            }
            for (var c in $scope.categories) {
                var cat = $scope.categories[c];
                if (cat.id == parent_id && cat.parent) {
                    return cat.name + " >> " + $scope.makeCategoryTree(cat.parent);
                } else {
                    return cat.name + " >> ";
                }
            }
        };
    });
});