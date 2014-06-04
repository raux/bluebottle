/*
 Controllers
 */


App.TaskListController = Em.ArrayController.extend({
    needs: ['taskSearchForm']
});


App.TaskSearchFormController = Em.ObjectController.extend({
    needs: ['taskList'],

    init: function(){
        var form =  App.TaskSearch.createRecord();
        this.set('model', form);
        this.updateSearch();
    },

    rangeStart: function(){
        return this.get('page') * 8 -7;
    }.property('controllers.taskList.model.length'),

    rangeEnd: function(){
        return this.get('page') * 8 -8 + this.get('controllers.taskList.model.length');
    }.property('controllers.taskList.model.length'),

    hasNextPage: function(){
        var next = this.get('page') * 8 -7;
        var total = this.get('controllers.taskList.model.meta.total');
        return (next < total);
    }.property('controllers.taskList.model.meta.total'),

    hasPreviousPage: function(){
        return (this.get('page') > 1);
    }.property('page'),

    nextPage: function(){
        this.incrementProperty('page');
    },

    previousPage: function(){
        this.decrementProperty('page');
    },

    sortOrder: function(order) {
        this.set('ordering', order);
    },

    orderedByNewest: function(){
        return (this.get('ordering') == 'newest');
    }.property('ordering'),
    orderedByDeadline: function(){
        return (this.get('ordering') == 'deadline');
    }.property('ordering'),

    clearForm: function(sender, key) {
        this.set('model.text', '');
        this.set('model.skill', null);
        this.set('model.status', null);
        this.set('model.country', null);
    },

    updateSearch: function(sender, key){
        if (key != 'page') {
            // If the query changes we should jump back to page 1
            this.set('page', 1);
        }
        if (this.get('model.isDirty') ) {
            var list = this.get('controllers.taskList');
            var controller = this;

            var query = {
                'page': this.get('page'),
                'ordering': this.get('ordering'),
                'status': this.get('status'),
                'country': this.get('country'),
                'text': this.get('text'),
                'skill': this.get('skill.id')
            };
            var tasks = App.TaskPreview.find(query);
            list.set('model', tasks);
        }
    }.observes('text', 'skill', 'status', 'country', 'page', 'ordering')


});


App.IsProjectOwnerMixin = Em.Mixin.create({
    isProjectOwner: function() {
        var username = this.get('controllers.currentUser.username');
        var ownername = this.get('controllers.project.model.owner.username');
        if (username) {
            return (username == ownername);
        }
        return false;
    }.property('controllers.project.model.owner', 'controllers.currentUser.username')
});


App.CanEditTaskMixin = Em.Mixin.create({
    canEdit: function() {
        var username = this.get('controllers.currentUser.username');
        var author_name = this.get('author.username');
        if (username) {
            return (username == author_name);
        }
        return false;
    }.property('author', 'controllers.currentUser.username')
});

App.ProjectTasksIndexController = Em.ArrayController.extend(App.IsProjectOwnerMixin, {
    needs: ['currentUser', 'project']
});


App.TaskController = Em.ObjectController.extend(App.CanEditTaskMixin, App.IsAuthorMixin, {
    needs: ['currentUser'],

	// you can apply to a task only if:
	// the task is not closed, realized or completed
	// (strange behaviour since completed is not a status but just a label)
	// and if:
	// you are not a already a member or if you already applied
	isApplicable: function(){
		var model = this.get('model');
        if (model.get('isStatusClosed') || model.get('isStatusRealized') || model.get('isStatusCompleted')){
            return false;
        }
        if (this.get('isMember')) {
            return false;
        }
        if (this.get('acceptedMemberCount') >=  this.get('people_needed')) {
            return false;

        }
        return true;
	}.property('status', 'isMember', 'model.isStatusClosed', 'model.isStatusRealized', 'model.isStatusCompleted',
		'model.@members.isStatusAccepted'),

    acceptedMemberCount: function(){
        return (this.get('members').filterBy('isAccepted').get('length'));
    }.property('model.members.@each.status'),

    isMember: function() {
        var user = this.get('controllers.currentUser.username');
        var isMember = false;
        this.get('model.members').forEach(function(member) {
            var mem = member.get('member.username');
            if (mem == user) {
                isMember =  true;
            }
        });
        return isMember;
    }.property('members.@each.member.username', 'controllers.currentUser.username'),

    canUpload: function(){
        return (this.get('isMember') || this.get('isAuthor'));
    }.property('isMember', 'isAuthor'),

    acceptedMembers: function() {
      return this.get('model').get('members').filterBy('isStatusAccepted', true);
    }.property('members.@each.member.isStatusAccepted'),

    notAcceptedMembers: function() {
      return this.get('model').get('members').filterBy('isStatusAccepted', false);
    }.property('members.@each.member.isStatusAccepted')

});


App.TaskActivityController = App.TaskController.extend({
    needs: ['task', 'currentUser', 'taskMember'],

    canEditTask: function() {
        var user = this.get('controllers.currentUser.username');
        var author_name = this.get('controllers.task.author.username');
        if (username) {
            return (username == author_name);
        }
        return false;
    }.property('controllers.task.author', 'controllers.currentUser.username'),

});

App.TaskIndexController = Em.ArrayController.extend({
    needs: ['task', 'currentUser'],
    perPage: 5,
    page: 1,
    remainingItemCount: function(){
        if (this.get('meta.total')) {
            return this.get('meta.total') - (this.get('page')  * this.get('perPage'));
        }
        return 0;
    }.property('page', 'perPage', 'meta.total'),

    canLoadMore: function(){
        var totalPages = Math.ceil(this.get('meta.total') / this.get('perPage'));
        return totalPages > this.get('page');
    }.property('perPage', 'page', 'meta.total'),

    actions: {
        showMore: function() {
            var controller = this;
            var page = this.incrementProperty('page');
            var id = this.get('controllers.task.model.id');
            App.WallPost.find({'parent_type': 'task', 'parent_id': id, page: page}).then(function(items){
                controller.get('model').pushObjects(items.toArray());
            });
        }
    },

    canAddMediaWallPost: function() {
        var username = this.get('controllers.currentUser.username');
        var ownername = this.get('controllers.task.model.author.username');
        if (username) {
            return (username == ownername);
        }
        return false;
    }.property('controllers.task.model.author', 'controllers.currentUser.username')

});


App.TaskMemberController = Em.ObjectController.extend({
    needs: ['task', 'currentUser'],

    isStatusApplied: function(){
        return this.get('status') == 'applied';
    }.property('status'),

    isStatusAccepted: function(){
        return this.get('status') == 'accepted';
    }.property('status'),

    isStatusInProgress: function(){
        return this.get('status') == 'in progress';
    }.property('status'),

    isStatusClosed: function(){
        return this.get('status') == 'closed';
    }.property('status'),

    isStatusRealized: function(){
        return this.get('status') == 'realized';
    }.property('status'),

    isCurrentUser: function(){
        var currentUser = this.get('controllers.currentUser.username');
        var member = this.get('member.username');
        if (member == currentUser){
            return true;
        }
        return false;
    }.property(),

    canWithdraw: function(){
        if (this.get('isCurrentUser') && (this.get('isStatusAccepted') || this.get('isStatusApplied')) ){
            return true;
        }
        return false;
    }.property(),

    actions: {
        withdrawTaskMember: function(member){
           member.deleteRecord()
           member.save()

        },
        testing: function(memer){
            console.log("testing!");
        }
    }
});

App.MyTaskMemberController = Em.ObjectController.extend({
    actions: {
        editTimeSpent: function() {
            this.set('isEditing', true);
            console.log(this.get('itemController'));
        }
    },

    isEditing: false
});

App.TaskNewController = Em.ObjectController.extend({
    needs: ['currentUser', 'taskIndex'],
    createTask: function(event){
        var controller = this;
        var task = this.get('content');
        task.on('didCreate', function(record) {
            controller.transitionToRoute('task', task);
        });
        task.on('becameInvalid', function(record) {
            // controller.set('errors', record.get('errors'));
            // Ember-data currently has no clear way of dealing with the state
            // loaded.created.invalid on server side validation, so we transition
            // to the uncommitted state to allow resubmission
            record.transitionTo('loaded.created.uncommitted');
        });

        task.save();
    }
});


App.TaskEditController = App.TaskNewController.extend({
    updateTask: function(event){
        var controller = this;
        var task = this.get('content');
        if (task.get('isDirty') == false){
            controller.transitionToRoute('task', task);
        }
        task.on('didUpdate', function(record) {
            controller.transitionToRoute('task', task);
        });
        task.on('becameInvalid', function(record) {
            controller.set('errors', record.get('errors'));
        });
        task.save();
    },
    cancelChangesToTask: function(event){
        var task = this.get('content');
        //Don't do a rollback on the object directly, but, via the transaction
        task.get('transaction').rollback();
        this.transitionToRoute('task', task);
    }

});


App.TaskPreviewController = Em.ObjectController.extend({
});


App.TaskMemberEditController = Em.ObjectController.extend({
});


App.TaskFileNewController = Em.ObjectController.extend({
    addFile: function(file) {
        this.set('model.file', file);
    }
});

