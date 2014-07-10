/*
*  Views
*/

App.SignupView = App.FormView.extend({
    keyPress: function (evt) {
        var code = evt.which;
        // If enter key pressed
        if (code == 13) {
            evt.preventDefault();
            this.get('controller').send('signup');
        }
    }
});

App.UserModalView = App.FormView.extend({
    templateName: 'user_modal'
});

App.LoginView = App.FormView.extend({
    templateName: 'login',
    
    next: function() {
        return  String(window.location);
    }.property(),

    keyPress: function (evt) {
        var code = evt.which;
        // If enter key pressed
        if (code == 13) {
            evt.preventDefault();
            this.get('controller').send('login');
        }
    }
});

App.PasswordResetView = App.FormView.extend({
    clearForm: function () {
        var controller = this.get('controller');

        controller.set('new_password1', null);
        controller.set('new_password2', null);
        controller.set('error', null);
    }.on('willInsertElement'),

    next: function() {
        return  String(window.location);
    }.property()

});

App.PasswordRequestView = App.FormView.extend({});


App.ItemSelectView = Em.Select.extend({
    optionValuePath: "content.id",
    optionLabelPath: "content.name",
    prompt: "Pick an item"
});

App.DisableAccountView = App.FormView.extend({
     templateName: 'disable'

});

