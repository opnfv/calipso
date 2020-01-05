///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
/*
 * Template Component: EnvKubeInfo
 */

import { Template } from 'meteor/templating';
import * as R from 'ramda';

import { createInputArgs } from '/imports/ui/lib/input-model';

import './env-kube-info.html';

/*
 * Events
 */

Template.EnvKubeInfo.events({
    'click .sm-next-button': function () {
        let instance = Template.instance();
        instance.data.onNextRequested();
    },

    'click .js-test-connection' : function (e, instance) {
        instance.data.onTestConnection();
    },
});

/*
 * Helpers
 */

Template.EnvKubeInfo.helpers({
    createInputArgs: createInputArgs,

    markIfDisabled: function () {
        let instance = Template.instance();
        let attrs = {};
        if (instance.data.disabled) {
            attrs = R.assoc('disabled', true, attrs);
        }

        return attrs;
    }
});