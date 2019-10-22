import { createActions } from "reduxsauce";

const { Types, Creators } = createActions({
  setState: ["payload"],
  loadCategories: null,
}, {prefix: 'C_'});

export const types = Types;
export default Creators;
