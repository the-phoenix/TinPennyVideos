import { createReducer } from "reduxsauce";
import { types } from "./actions";

export const INITIAL_STATE = {
  results: null,
  error: null,
  loading: false,
};

export default createReducer(INITIAL_STATE, {
  [types.SET_STATE]: (state, { payload }) => ({ ...state, ...payload })
});
