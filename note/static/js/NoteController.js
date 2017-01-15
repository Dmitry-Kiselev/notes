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
        $scope.files = [];


        angular.element(document).ready(function() {
            // Initialize collapse button
            $("#sidenav-btn").sideNav();
            $('.modal').modal();
            $('select').material_select();
            $('input#title').characterCounter();
            $('.tooltipped').tooltip({delay: 50});

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
                    // make the object to store all usernames in a form needed to use with autocomplete
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
                /*
                this function must be called after page load,
                because there are the bug then using
                materialize with angular: statement must be
                activated after angular loaded data
                to populate that statement
                 */
                $('select').material_select();
            };

            $scope.sendNote = function() {
                /*
                 before send, function will choose proper HTTP method
                 depending on object fields: only server can give id field to the note,
                 so if it has it - we send existing note, we will use PUT method.
                 */
                if ($scope.curNote.id) { // existing notes have id field
                    noteFactory.notesManager().update({
                        id: $scope.curNote.id
                    }, $scope.curNote, function(response) {
                        // find the old note in the list and replace with a new one
                        var index = $scope.notes.findIndex(x => x.id == $scope.curNote.id);
                        $scope.notes[index] = response;
                    });
                    var index = $scope.notes.findIndex(x => x.id == $scope.curNote.id);
                    $scope.notes[index] = $scope.curNote;
                    $scope.showInfo('Note updated');
                } else {
                    noteFactory.notesManager().save($scope.curNote, function(response) {
                        // use response to provide correct and complete object with all required fields including id
                        $scope.notes.push(response);
                        $scope.showInfo('Note created');
                    });
                }
                $scope.curNote = {};
                $('#noteModal').modal('close');
            };

            $scope.deleteNote = function(id) {
                /*
                delete note from server and the note list
                 */
                noteFactory.notesManager().delete({
                    id: id
                });
                var index = $scope.notes.findIndex(x => x.id == id);
                $scope.notes.pop(index);
                $scope.showInfo('Note deleted');
            };


            $scope.editNote = function(id) {
                var index = $scope.notes.findIndex(x => x.id == id); // find note object for editing by id
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
                setTimeout(function() {
                    Materialize.updateTextFields(); // to fix trouble with the labels overlapping prefilled content
                }, 500);
            };

            $scope.sendLabel = function() {
                // same as for sendNote
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

            // for multiple files upload:
            $scope.uploadFiles = function(type, files) {
                var url = '';
                var dataObj = {};
                // choose url depending on file type
                if (type == 'file') {
                    url = '/files/';
                }
                if (type == 'image') {
                    url = '/images/';
                }
                if (files && files.length) {
                    for (var i = 0; i < files.length; i++) {
                        if (type == 'file') {
                            dataObj = {
                                file: files[i]
                            };
                        }
                        if (type == 'image') {
                            dataObj = {
                                image: files[i]
                            };
                        }
                        Upload.upload({
                            data: dataObj,
                            url: url,
                            method: 'POST'
                        }).then(function(response) {
                            if (type == 'file') {
                                $scope.curNote.files.push(response.data);
                            }
                            if (type == 'image') {
                                $scope.curNote.images.push(response.data);
                            }
                        });
                    }
                }
            };

            $scope.setFilter = function(name) {
                /*
                to change note's filter;
                can be used to filter notes by labels or categories
                 */
                $scope.searchText = name;
            };

            $scope.noteDetail = function(id) {
                // find note and display it in detailModal
                var index = $scope.notes.findIndex(x => x.id == id);
                $scope.curNote = $scope.notes[index];
                $('#detailModal').modal();
            };

            $scope.clearCurNote = function() {
                $scope.curNote = {};
            };

            $scope.shareNote = function(id) {
                /*
                create object to store shared note's id and user to share it with
                user field populates by using mg-model directive in template
                 */
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
                // to check is the note shared with someone
                // must have array, and array must be not empty
                if (item.shared_with && item.shared_with.length != 0) {
                    $scope.shareFlag = true;
                    return true;
                }
            };

            $scope.deleteShare = function(note_id, user_id) {
                var note_index = $scope.notes.findIndex(x => x.id == note_id);
                var index = $scope.notes[note_index].shared_with.indexOf(user_id);
                if (index >= 0) {
                    $scope.notes[note_index].shared_with.splice(index, 1); // delete sharing relation from the note object
                }
                var shareRelation = {
                    'note': note_id,
                    'user': user_id
                };
                noteFactory.userManager().delete(shareRelation); // // delete sharing relation from the server
                $scope.showInfo('Deleted');
            };

            $scope.deleteContent = function(type, id) {
                /*
                to delete any type of content created by the user except notes.
                Notes have their own function.
                Deletes content from server and client sides.
                 */
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
                /*
                Categories have a tree structure, so we need to display it in some way to the user.
                Because there are no widgets which can do that, easiest way is display all hierarchy
                in the category name.
                 */

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
                /*
                use the same modal to display different types of content
                 */
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
            };

            $scope.confirmAdd = function(type, files) {
                if ($scope.curNote.files && $scope.curNote.files.length && type == 'file') {
                    var addFiles = true;
                }
                if ($scope.curNote.images && $scope.curNote.images.length && type == 'image') {
                    var addImg = true;
                }
                if (addFiles || addImg) {
                    var replace = confirm('Add new files to existing ones? Otherwise old files will be deleted.');
                    if (replace) {
                        $scope.uploadFiles(type, files);
                        $scope.files = [];
                    }
                    else {
                        if (addFiles){$scope.curNote.files = [];}
                        if (addImg){$scope.curNote.images = [];}
                        $scope.uploadFiles(type, files);
                        $scope.files = [];
                    }
                } else {
                    if (!$scope.curNote.files) {
                        $scope.curNote.files = [];
                    }
                    if (!$scope.curNote.images) {
                        $scope.curNote.images = [];
                    }
                    $scope.uploadFiles(type, files);
                    $scope.files = [];
                }

            }
        });
    });