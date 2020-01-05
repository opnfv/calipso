///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import { Mongo } from 'meteor/mongo';
import { SimpleSchema } from 'meteor/aldeed:simple-schema';
import * as R from 'ramda';
import { Constants } from '../constants/constants'
import {toOptions} from "../../lib/utilities";

export const EnvironmentOptions =
    new Mongo.Collection('environment_options', { idGeneration: 'MONGO' });

let schema = {
    _id: { type: { _str: { type: String, regEx: SimpleSchema.RegEx.Id } } },
    environment_type: { type: String },
    distributions: { type: [String] },
    distribution_versions: { type: [String] },
    mechanism_drivers: { type: [String] },
    type_drivers: { type: [String] },
};

EnvironmentOptions.schema = schema;
EnvironmentOptions.attachSchema(schema);

EnvironmentOptions.getDistributionsByEnvType = function (env_type) {
    return toOptions(
        R.flatten(
            R.reduce((acc, option) => {
                    return R.append(
                        R.ifElse(R.isNil, R.always([]), R.prop('distributions'))(option),
                        acc
                    )
                },
                [],
                EnvironmentOptions.find({environment_type: env_type}).fetch()
            )
    ));
};

EnvironmentOptions.getOptions = function(distribution, field) {
    if (distribution) {
        return toOptions(
            R.ifElse(R.isNil, R.always([]), R.prop(field)) (
                EnvironmentOptions.findOne({ distributions: distribution })
            )
        );
    }
    else {
        return Constants.getByName(field);
    }
};