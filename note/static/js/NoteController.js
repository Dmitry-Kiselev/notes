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
        $scope.curCategory = {};
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
                    $scope.showInfo('Note updated');
                } else {
                    noteFactory.notesManager().save($scope.curNote, function(response) {
                        $scope.notes.push(response);
                        $scope.showInfo('Note created');
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
                $scope.showInfo('Note deleted');
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
                    $scope.showInfo('Label updated');
                } else {
                    noteFactory.labelsManager().save($scope.curLabel, function(response) {
                        $scope.labels.push(response);
                    });
                    $scope.showInfo('Label created');
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
                    $scope.showInfo('Note shared with ' + $scope.shareObj.user);
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
                $scope.showInfo('Note deleted');
            };

            $scope.deleteContent = function(type, id) {
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
                if (type == 'image') {
                    manager = noteFactory.imagesManager();
                    var index = $scope.images.findIndex(x => x.id == id);
                    $scope.images.pop(index);
                }
                if (type == 'file') {
                    manager = noteFactory.filesManager();
                    var index = $scope.files.findIndex(x => x.id == id);
                    $scope.files.pop(index);
                }
                manager.delete({
                    id: id
                });
                $scope.showInfo('Deleted');
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

            $scope.sendCategory = function() {
                noteFactory.categoriesManager().save($scope.curCategory, function(response) {
                    $scope.categories.push(response);
                });
                $scope.curCategory = {};
                $scope.showInfo('Category created');
            };

            $scope.editUserContentModal = function(type) {
                if (type == 'labels') {
                    $scope.editModalLabels = true;
                    $scope.editModalCategories = false;
                    $scope.editModalFiles = false;
                    $scope.editModalImages = false;
                }
                if (type == 'categories') {
                    $scope.editModalCategories = true;
                    $scope.editModalLabels = false;
                    $scope.editModalFiles = false;
                    $scope.editModalImages = false;
                }
                if (type == 'images') {
                    $scope.images = noteFactory.imagesManager().query();
                    $scope.editModalCategories = false;
                    $scope.editModalLabels = false;
                    $scope.editModalFiles = false;
                    $scope.editModalImages = true;
                }
                if (type == 'files') {
                    $scope.files = noteFactory.filesManager().query();
                    $scope.editModalCategories = false;
                    $scope.editModalLabels = false;
                    $scope.editModalFiles = true;
                    $scope.editModalImages = false;
                }
                $('#editContent').modal('open');
            };

            $scope.showInfo = function(message) {
                // Materialize.toast(message, displayLength, className, completeCallback);
                Materialize.toast(message, 4000); // 4000 is the duration of the toast
            }

        });
    });