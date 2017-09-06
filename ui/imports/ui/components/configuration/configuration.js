/*
 * Template Component: Configuration 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
//import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';

import { save } from '/imports/api/configurations/methods';
import { Configurations } from '/imports/api/configurations/configurations';
        
import './configuration.html';     
    
/*  
 * Lifecycles
 */   
  
Template.Configuration.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    model: Configurations.schema.clean({}),
    actionResult: 'none',
    message: null,
  });

  /*
  instance.autorun(function () {
    let data = Template.currentData();

    new SimpleSchema({
    }).validate(data);
  });
  */

  instance.autorun(function () {
    instance.subscribe('configurations?user');
    Configurations.find({user_id: Meteor.userId()}).forEach((conf) => {
      instance.state.set('model', conf);
    });
  });
});  

/*
Template.Configuration.rendered = function() {
};  
*/

/*
 * Events
 */

Template.Configuration.events({
  'click .js-submit-button': function (event, instance) {
    event.preventDefault(); 
    let msgsViewBackDelta = instance.$('.cl-msgs-view-back-delta')[0].value;
    saveForm(instance, msgsViewBackDelta);
  }
});
   
/*  
 * Helpers
 */

Template.Configuration.helpers({    
  getModelField: function (fieldName) {
    let instance = Template.instance();
    return R.path([fieldName], instance.state.get('model'));
  },

  getState: function (key) {
    let instance = Template.instance();
    return instance.state.get(key);
  },

  isActionError: function () {
    let instance = Template.instance();
    return instance.state.get('actionResult') === 'error';
  },

  isActionSuccess: function () {
    let instance = Template.instance();
    return instance.state.get('actionResult') === 'success';
  },

  durationHumanize: function (duration) {
    return moment.duration(duration).humanize();
  }
}); // end: helpers

function saveForm(instance, msgsViewBackDelta) {
  instance.state.set('actionResult', 'none');
  instance.state.set('message', null);

  save.call({
    messages_view_backward_delta: msgsViewBackDelta
  }, (error) => {
    if (error) {
      instance.state.set('actionResult', 'error');
      if (typeof error === 'string') {
        instance.state.set('message', error);
      } else {
        instance.state.set('message', error.message);
      }

      return;
    } 

    instance.state.set('actionResult', 'success');
    instance.state.set('message', 'record has been updated succesfuly');
  });
}
