import { all, takeEvery, put, call } from "redux-saga/effects";

import {loadVideos, loadIndividualVideo} from "services/api";
import { types } from "./actions";

export function* LOAD_VIDEOS() {
  yield put({
    type: types.SET_STATE,
    payload: {
      loading: true
    }
  });

  const response = yield call(loadVideos);
  if (response) {
    yield put({
      type: types.SET_STATE,
      payload: response.data
    });
  }

  yield put({
    type: types.SET_STATE,
    payload: {
      loading: false
    }
  });
}

export function* LOAD_INDIVIDUAL_VIDEO({videoId}) {
  console.log('whats this?', videoId);
  yield put({
    type: types.SET_STATE,
    payload: {
      loading: true
    }
  });

  const response = yield call(loadIndividualVideo, [videoId]);
  if (response) {
    yield put({
      type: types.SET_STATE,
      payload: {
        individual: response.data
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
    takeEvery(types.LOAD_VIDEOS, LOAD_VIDEOS),
    takeEvery(types.LOAD_INDIVIDUAL_VIDEO, LOAD_INDIVIDUAL_VIDEO)
  ]);
}
