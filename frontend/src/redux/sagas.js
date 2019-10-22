import { all } from "redux-saga/effects";

import auth from "./auth/saga";
import category from "./category/saga";
import video from "./video/saga";

export default function* rootSaga() {
  console.log('Root saga invoked!');

  yield all([auth(), category(), video()]);
}
