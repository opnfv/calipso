import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import calipsoApp from '/imports/ui/reducers/index';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
  calipsoApp,
  composeEnhancers(
    applyMiddleware(
      thunk
    )
  )
);

export {
  store
};
