import { createReducer } from "reduxsauce";
import { types } from "./actions";

export const INITIAL_STATE = {
  authorized: false,
  token: null,
  user: null,
  loading: false,
  error: null,
};

export default createReducer(INITIAL_STATE, {
  [types.SET_STATE]: (state, { payload }) => ({ ...state, ...payload })
});
