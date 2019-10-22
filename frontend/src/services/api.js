import axios from "axios";

const _createClient = baseUrl => axios.create({
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
});

const client = _createClient(process.env.API_BASEURL || "http://localhost:8000/api/v1");

export const login = (email, password) => client.post("/auth/login/", { email, password });

export const verifyToken = (token) => client.post("/token-verify/", { token });

export const loadCategories = () => client.get("/media/categories/");

export const loadVideos = () => client.get("/media/videos/");

export const loadIndividualVideo = videoId => client.get(`/media/videos/${videoId}/`);
