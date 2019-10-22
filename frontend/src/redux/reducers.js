import { combineReducers } from "redux";
import { connectRouter } from "connected-react-router";
import { reducer as formReducer } from "redux-form";

import auth from "./auth/reducer";
import category from "./category/reducer";
import video from "./video/reducer";


export default history =>
  combineReducers({
    form: formReducer,
    router: connectRouter(history),
    auth,
    category,
    video
  });
