///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
/* Created by oashery on 3/2/2016. Modified by sisakov on 9/7/2016*/
import * as R from 'ramda';
import { Environments } from '/imports/api/environments/environments';
import { parseReqId } from '/imports/lib/utilities';

/*
 *
 */

if (Meteor.isClient){
  Accounts.onLogin(function () {
    Router.go('/Dashboard');
  });

  Accounts.onLogout(function () {
    Router.go('/');
  });
}

Router.configure({
  layoutTemplate: 'main',
  loadingTemplate: 'loading'
});

if (Meteor.isClient) {
  let originalDispatch = Router.dispatch;

  Router.dispatch = function (_href, _a, _onDispatchComplete) {
    let that = this;
    let args = arguments;
    let controller = that.current();
    if (controller) {
      let isDirty = Session.get('isDirty');
      let needsConfirmation = controller.state.get('needsConfirmation');

      if (needsConfirmation && isDirty) {
        let confirmResult = confirm('Changes are not saved. Are you sure you want to leave?');
        if (confirmResult) {
          Session.set('isDirty', false);
        } else {
          let loc = Iron.Location.get();
          loc.cancelUrlChange();
          return;
        }
      }
    }

    originalDispatch.apply(that, args);
  };
}

function confirm(msg) {
  return window.confirm(msg);
}
/*
 * Hooks
 */

Router.onBeforeAction(function () {
  if (Meteor.userId()) {
    this.next();
  } else {
    this.layout('landing');
    this.render('landing');
  }
});

/*
 * Routes
 */

Router.route('/', {
  name: 'landing',
  path: '/',
  action: function () {
    if (Meteor.userId()) {
      Router.go('/Dashboard');
    }
    if (this.ready())
      this.layout('landing');
    else
      this.render('loading');
  }
});

Router.route('home', {
  path: '/home',
  /* refactor to component. home not in use ?
  waitOn: function () {
      return Meteor.subscribe('inventory');
  },
  */
  action: function () {
    if (this.ready()){

      this.state.set('envName', this.params.query.env);
      /*
                  if(query){
                          //return Inventory.find({$where: "this.id_path.match('^/WebEX-Mirantis@Cisco/')"});
                          console.log(query);
                          this.render('home', {
                              data: function () {
                                  return Inventory.find({environment: query, parent_id: query});
                              }
                          });
                          //
                  }
      */

      // if the sub handle returned from waitOn ready() method returns
      // true then we're ready to go ahead and render the page.
      this.render('home');

    }
    else{
      this.render('loading');
    }
  }
});

Router.route('getstarted', {
  name: 'getstarted',
  path: '/getstarted'
});

Router.route('/wizard', function () {
  this.state.set('env', null);
  Session.set('wizardEnv', null);
  this.render('EnvironmentWizard');
});

Router.route('/wizard/:env', function () {
  this.state.set('env', this.params.env);
  Session.set('wizardEnv', this.params.env);
  this.render('EnvironmentWizard');
});

Router.route('/scans-list', function () {
  this.render('ScansList');
}, { });

Router.route('/scheduled-scans-list', function () {
  this.render('ScheduledScansList');
}, { 
  name: 'scheduled-scans-list',
  data: function () {
    //let that = this;
    let data = {};
    return data;
  }
});

Router.route('/link-types-list', function () {
  this.render('LinkTypesList');
}, { });

Router.route('/link-type', function () {
  this.render('LinkType');
}, { });

Router.route('/clique-types-list', function () {
  this.render('CliqueTypesList');
}, { });

Router.route('/clique-type', function () {
  this.render('CliqueType');
}, { });

Router.route('/clique-constraints-list', function () {
  this.render('CliqueConstraintsList');
}, { });

Router.route('/clique-constraint', function () {
  this.render('CliqueConstraint');
}, { });

Router.route('/messages-list', function () {
  this.render('MessagesList');
}, { });

Router.route('/user-settings', function () {
  this.render('UserSettings');
}, { });

Router.route('/message', function () {
  let that = this;
  let params = that.params;
  let query = params.query;

  this.render('Message', {
    data: function () {
      return {
        id: query.id,
        action: query.action
      };
    }
  });
}, { });

Router.route('/user-list', function () {
  this.render('UserList');
}, { });

Router.route('/user', function () {
  this.render('User');
}, { });

Router.route('/scanning-request', function () {
  this.render('ScanningRequest');
}, {
  name: 'scanning-request',
  data: function () {
    let that = this;

    let _id = 
      R.when(R.pipe(R.isNil, R.not), 
        (idObj) => R.prop('id', parseReqId(idObj))
      )(R.path(['params', 'query', '_id'], that));

    let data = {
      _id: _id,
      env: that.params.query.env,
      action: that.params.query.action,
    };

    return data;
  }
});


Router.route('/scheduled-scan', function () {
  this.render('ScheduledScan');
}, {
  name: 'scheduled-scan',
  data: function () {
    let that = this;

    let _id = 
      R.when(R.pipe(R.isNil, R.not), 
        (idObj) => R.prop('id', parseReqId(idObj))
      )(R.path(['params', 'query', '_id'], that));

    let data = {
      _id: _id,
      env: that.params.query.env,
      action: that.params.query.action,
    };

    return data;
  }
});

Router.route('/new-scanning', function () {
  this.render('NewScanning');
}, {
  name: 'new-scanning',
  data: function () {
    let that = this;

    let data = {
      env: that.params.query.env,
    };

    return data;
  }
});

Router.route('Dashboard', {
  name: 'Dashboard',
  path: '/Dashboard',
  /* eyaltask
  waitOn: function () {
          return Meteor.subscribe('inventory');
  },
  */
  action: function () {
    if (this.ready()){
      this.render('Dashboard');

    }
    else{
      this.render('loading');
    }
  }
});

Router.route('environment', {
  name: 'environment',
  path: '/environment/:_id',
  action: function () {
    if (this.ready()){
      this.render('Environment');
    }
    else{
      this.render('loading');
    }
  },
  data: function () {
    let that = this;

    let _id = parseReqId(that.params._id).id;
    let selectedNodeId = R.ifElse(R.isNil,
      R.always(null),
      R.pipe(
        R.curry(parseReqId),
        R.prop('id')
      )
    )(that.params.query.selectedNodeId);

    let data = { _id: _id };

    if (! R.isNil(selectedNodeId)) {
      data = R.assoc('selectedNodeId', selectedNodeId, data);
    }

    let refresh = that.params.query.r;
    if (! R.isNil(refresh)) {
      data = R.assoc('refresh', refresh, data);
    }

    return data;
  }
});


Router.route('migrateEnvToUserId', {
  name: 'migrateEnvToUserId',
  where: 'server',
  action: function () {
    console.log('migrate env to user id');

    //let request = this.request;
    let response = this.response;

    let envs = Environments.find({}).fetch();
    R.forEach((env) => {
      console.log('found env: ' + env.name + ' ' + R.toString(env._id));

      let user = Meteor.users.findOne({ username: env.user }); 
      if (R.isNil(user)) { 
        console.log('not migrated: ' + env.name);    
        return;
      }
      console.log('found user: ' + user._id + ' ' + user.username);    

      try {
        let result = Environments.update(
          { _id : env._id },
          {
            $set: {
              user: user._id
            }
          });
        console.log('result', R.toString(result));
        console.log('migrated: ' + env.name);    
      } catch(e) {
        console.log('exception', R.toString(e));
      }

    }, envs);

    response.end('migration end');
  }
});
