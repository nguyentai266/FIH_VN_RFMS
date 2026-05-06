
import axios from 'axios';


const axiosClient = axios.create({
  baseURL: (import.meta as any).env.VITE_API_BASE_URL, 
  
});

axiosClient.interceptors.response.use(
  (response) => {

    return response.data;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosClient;