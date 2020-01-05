###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
"""
Do a deep merge of dictionariesi,
recursively merging dictionaries with boltons.iterutils.remap

Taken from:
https://gist.github.com/mahmoud/db02d16ac89fa401b968


This is an extension of the technique first detailed here:
http://sedimental.org/remap.html#add_common_keys
In short, it calls remap on each container, back to front,
using the accumulating previous values as the default for
the current iteration.
"""

from boltons.iterutils import remap, get_path, default_enter, default_visit


def remerge(target_list, sourced=False):
    """
    Takes a list of containers (e.g., dicts) and merges them using
    boltons.iterutils.remap. Containers later in the list take
    precedence (last-wins).
    By default, returns a new, merged top-level container. With the
    *sourced* option, `remerge` expects a list of (*name*, container*)
    pairs, and will return a source map: a dictionary mapping between
    path and the name of the container it came from.
    """

    if not sourced:
        target_list = [(id(t), t) for t in target_list]

    ret = None
    source_map = {}

    def remerge_enter(path, key, value):
        new_parent, new_items = default_enter(path, key, value)
        if ret and not path and key is None:
            new_parent = ret
            try:
                cur_val = get_path(ret, path + (key,))
            except KeyError:
                pass
            else:
                # TODO: type check?
                new_parent = cur_val

        if isinstance(value, list):
            # lists are purely additive.
            # See https://github.com/mahmoud/boltons/issues/81
            new_parent.extend(value)
            new_items = []

        return new_parent, new_items

    for t_name, target in target_list:
        if sourced:
            def remerge_visit(path, key, value):
                source_map[path + (key,)] = t_name
                return True
        else:
            remerge_visit = default_visit

        ret = remap(target, enter=remerge_enter, visit=remerge_visit)

    if not sourced:
        return ret
    return ret, source_map
