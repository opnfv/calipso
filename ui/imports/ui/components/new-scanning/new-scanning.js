/*
 * Template Component: NewScanning 
 */
    
//import { Meteor } from 'meteor/meteor'; 
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';
        
import './new-scanning.html';     
    
/*  
 * Lifecycles
 */   
  
Template.NewScanning.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    env: null,
  });

  instance.autorun(function (env) {
    let data = Template.currentData();
    new SimpleSchema({
      env: { type: String, optional: true },
    }).validate(data);

    instance.state.set('env', env);
  });
});  

/*
Template.NewScanning.rendered = function() {
};  
*/

/*
 * Events
 */

Template.NewScanning.events({
});
   
/*  
 * Helpers
 */

Template.NewScanning.helpers({    
  argsScanningRequest: function (env) {
    return {
      action: 'insert',
      env: env,
    };
  },

  argsScheduledScan: function (env) {
    return {
      action: 'insert',
      env: env,
    };
  },
}); // end: helpers


