///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                         /
// Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others       /
//                                                                            /
// All rights reserved. This program and the accompanying materials           /
// are made available under the terms of the Apache License, Version 2.0      /
// which accompanies this distribution, and is available at                   /
// http://www.apache.org/licenses/LICENSE-2.0                                 /
///////////////////////////////////////////////////////////////////////////////
import * as R from 'ramda';

import * as actions from '/imports/ui/actions/graph-tooltip-window.actions';

const defaultState = {
  tooltipIcon: '',
  label: '',
  title: '',
  left: 0,
  top: 0,
  show: false
};

export function reducer(state = defaultState, action) {
  let tooltipIconStr = "icon-layers-C.svg";
  let attrsStr = "";

  switch (action.type) {
    case actions.ACTIVATE_GRAPH_TOOLTIP_WINDOW:
      action.payload.attributes.forEach(function (attr) {
        let text = JSON.stringify(attr, null, 2)
          // .toString()
          // .replace(/\,/g,'<BR>')
          .replace(/\{/g, '')
          .replace(/\}/g, '')
          .replace(/"/g, '')
          .replace(/\[dot\]/g, '.');

        // *** Styling the ToolTip window ******
        if (!R.isNil(text)) {
          let keyValueStr = text.split(":");
          if (keyValueStr[0] !== '') {
            let keyName = keyValueStr[0];
            let valueStr = text.replace(keyName + ':', '');
            keyName = keyName.replace('_', ' ');

            if (keyName.trim().toLowerCase() == "status") {
              let statusDesc = keyValueStr[1].trim().toLowerCase();
              switch (statusDesc) {
                case 'ok':
                  tooltipIconStr = 'icon-alert-info-white.svg';
                  break;
                case 'warning':
                  tooltipIconStr = 'icon-alert-warning-white.svg';
                  break;
                case 'error':
                  tooltipIconStr = 'icon-alert-error-white.svg';
                  break;
              }
            }

            attrsStr += '<div class="attr-container">'

            let clsKey = 'attr-tooltip-keyname'
            attrsStr += `<div class=${clsKey}>` + keyName + '</div>';

            let clsValue = 'attr-tooltip-value'
            attrsStr += `<div class=${clsValue}>` + valueStr + '</div>';
            attrsStr += '</div>'
          }
          else {
            let cls = 'attr-' + Object.keys(attr)[0];
            attrsStr += `<div class=${cls}>` + text + '</div>';
          }
        }
        // **************************************
      });
      // TODO
      // attrsStr = JSON.stringify(action.payload.attributes, null, 4)
      //   .toString()
      //   .replace(/\,/g,'<BR>')
      //   .replace(/\[/g,'')
      //   .replace(/\]/g,'')
      //   .replace(/\{/g,'')
      //   .replace(/\}/g,'')
      //   .replace(/"/g,'');

      return R.merge(state, {
        tooltipIcon: tooltipIconStr,
        label: action.payload.label,
        title: attrsStr,
        left: action.payload.left,
        top: action.payload.top - 28,
        show: true
      });

    case actions.CLOSE_GRAPH_TOOLTIP_WINDOW:
      return R.assoc('show', false, state);

    default:
      return state;
  }
}
