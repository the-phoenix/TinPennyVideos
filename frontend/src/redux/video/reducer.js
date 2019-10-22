import { createReducer } from "reduxsauce";
import { types } from "./actions";

export const INITIAL_STATE = {
  count: -1,
  next: null,
  previous: null,
  results: null,
  individual: null,
  error: null,
  loading: false,
};

export default createReducer(INITIAL_STATE, {
  [types.SET_STATE]: (state, { payload }) => ({ ...state, ...payload })
});
