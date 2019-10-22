import { createBrowserHistory } from "history";
import { applyMiddleware, compose, createStore } from "redux";
import { routerMiddleware } from "connected-react-router";
import createSagaMiddleware from "redux-saga";
import { logger } from "redux-logger";

// import clients from "./clients";
import createRootReducer from "./redux/reducers";
import sagas from "./redux/sagas";

export const history = createBrowserHistory();

const sagaMiddleware = createSagaMiddleware();
const routeMiddleware = routerMiddleware(history);
const middlewares = [sagaMiddleware, routeMiddleware];
if (process.env.NODE_ENV === "development" && true) {
  middlewares.push(logger);
}

export function bootstrapSaga() {
  sagaMiddleware.run(sagas);
}

export default function configureStore(preloadedState) {
  const composeEnhancer =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose; // eslint-disable-line
  const store = createStore(
    createRootReducer(history),
    preloadedState,
    composeEnhancer(applyMiddleware(...middlewares))
  );

  // Hot reloading
  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept("./redux/reducers", () => {
      store.replaceReducer(createRootReducer(history));
    });
  }

  return store;
}
