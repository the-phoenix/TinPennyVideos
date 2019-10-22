import { all, takeEvery, put, call } from "redux-saga/effects";

import {loadCategories} from "services/api";
import { types } from "./actions";

export function* LOAD_CATEGORIES() {
  yield put({
    type: types.SET_STATE,
    payload: {
      loading: true
    }
  });

  const response = yield call(loadCategories);
  if (response) {
    yield put({
      type: types.SET_STATE,
      payload: {
        results: response.data
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


export default function* rootSaga() {
  yield all([
    takeEvery(types.LOAD_CATEGORIES, LOAD_CATEGORIES),
    LOAD_CATEGORIES() // run once on app load to get categories loaded
  ]);
}
