import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from "react-redux";
import configureStore, { history, bootstrapSaga } from "./configureStore";
import Router from "./router";

import './index.scss';
import * as serviceWorker from './serviceWorker';

const store = configureStore();
bootstrapSaga();

ReactDOM.render(
  <Provider store={store}>
    <Router history={history} />
  </Provider>
  , document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
