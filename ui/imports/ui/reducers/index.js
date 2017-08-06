import { combineReducers } from 'redux';

import { navigation } from './navigation';
import { searchInterestedParties } from './search-interested-parties';
import { reducer as environmentPanel } from './environment-panel.reducer';
import { reducer as i18n } from './i18n.reducer';
import { reducer as graphTooltipWindow } from './graph-tooltip-window.reducer';
import { reducer as vedgeInfoWindow } from './vedge-info-window.reducer';
import { reducer as mainApp } from './main-app.reducer';

const calipsoApp = combineReducers({
  api: combineReducers({
    navigation,
    searchInterestedParties,
    i18n
  }),
  components: combineReducers({
    mainApp: mainApp,
    environmentPanel,
    graphTooltipWindow,
    vedgeInfoWindow
  })
});

export default calipsoApp;
