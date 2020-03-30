import axios from "axios";

const defaultClient = (baseUrl) => (
  axios.create({
    baseURL: baseUrl,
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    transformResponse: [
      (data) => {
        if (typeof data === 'string') {
            try {
              data = JSON.parse(data);
            } catch (e) { 
              console.log('Parse error in intercept:', e);
              throw e;
            }
        }
        return data;
      },
      (data) => {
        // here you actually transform the response you would get by default when no transformation specified
        return data;
      },
    ]
  })
);

const clients = {
  default: {
    client: defaultClient("http://localhost:8000/api/v1"),
  },
};

export default clients;
