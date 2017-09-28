/*
 * Template Component: NewScanning 
 */
    
import * as R from 'ramda';
import { Template } from 'meteor/templating';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import { ReactiveDict } from 'meteor/reactive-dict';
import { ScheduledScans, subsScheduledScansEnv } from '/imports/api/scheduled-scans/scheduled-scans';
        
import './new-scanning.html';     
    
/*  
 * Lifecycles
 */   
  
Template.NewScanning.onCreated(function() {
  let instance = this;
  instance.state = new ReactiveDict();
  instance.state.setDefault({
    env: null,
    scheduledScanId: null
  });

  instance.autorun(function () {
    let data = Template.currentData();
    new SimpleSchema({
      env: { type: String, optional: true },
    }).validate(data);

    instance.state.set('env', data.env);
  });

  instance.autorun(function () {
    let env = instance.state.get('env');
    instance.subscribe(subsScheduledScansEnv, env);
    ScheduledScans.find({ environment: env }).forEach((schedule) => {
      instance.state.set('scheduledScanId', schedule._id);
    });
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
    let instance = Template.instance();
    let scheduledScanId = instance.state.get('scheduledScanId');
    let action = R.ifElse(R.isNil, R.always('insert'), R.always('update'))(scheduledScanId);

    return {
      action: action,
      env: env,
      _id: scheduledScanId,
    };
  },
}); // end: helpers


