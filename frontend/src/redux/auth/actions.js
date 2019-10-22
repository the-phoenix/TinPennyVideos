import { createActions } from "reduxsauce";

const { Types, Creators } = createActions({
  setState: ["payload"],
  login: ["email", "password"],
  logout: null,
}, {prefix: 'A_'});

export const types = Types;
export default Creators;
