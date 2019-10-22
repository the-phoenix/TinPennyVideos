import { all, takeEvery, put, call } from "redux-saga/effects";

import {login, verifyToken} from "services/api";
import {loadUserFromStore, storeCurrentUser, clearUser} from "services/store";
import { types } from "./actions";
import { INITIAL_STATE } from "./reducer";

export function* LOGIN({email, password}) {
  yield put({
    type: types.SET_STATE,
    payload: {
      error: null,
      loading: true
    }
  });

  try {
    const response = yield call(login, email, password);
    yield put({
      type: types.SET_STATE,
      payload: {
        ...response.data,
        authorized: true
      }
    });

    yield call(storeCurrentUser, response.data);
  } catch (e) {
    yield put({
      type: types.SET_STATE,
      payload: {
        error: e.response.data
      }
    });
  }

  yield put({
    type: types.SET_STATE,
    payload: {
      loading: false
    }
  });
}

export function* LOAD_FROM_STORE() {
  yield put({
    type: types.SET_STATE,
    payload: {
      loading: true
    }
  });

  const response = yield call(loadUserFromStore);
  if (response) {
    try {
      yield call(verifyToken, response.token);
      yield put({
        type: types.SET_STATE,
        payload: {
          ...response,
          authorized: true,
        }
      });
    } catch {
      console.log('Invalid token');
    }
  }

  yield put({
    type: types.SET_STATE,
    payload: {
      loading: false
    }
  });
}

export function* LOGOUT() {
  yield call(clearUser);
  yield put({
    type: types.SET_STATE,
    payload: INITIAL_STATE
  });
}

export default function* rootSaga() {
  yield all([
    takeEvery(types.LOGIN, LOGIN),
    takeEvery(types.LOGOUT, LOGOUT),
    LOAD_FROM_STORE() // run once on app load to get categories loaded
  ]);
}
