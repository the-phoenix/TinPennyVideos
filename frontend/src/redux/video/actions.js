import { createActions } from "reduxsauce";

const { Types, Creators } = createActions({
  setState: ["payload"],
  loadVideos: null,
  loadIndividualVideo: ["videoId"]
}, {prefix: 'V_'});

export const types = Types;
export default Creators;
