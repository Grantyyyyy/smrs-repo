import axios from 'axios';
import tokenServices from './tokenServices';


const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/', // Your Django API URL
  timeout: 10000,
});

apiClient.interceptors.request.use(
    (config) => {
        const token = tokenServices.getAccessToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);


apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try{
                const refreshToken = tokenServices.getRefreshToken();
                if (refreshToken) {
                    const response = await axios.get('http://localhost:8000/api/token/refresh/', {
                        refresh: refreshToken
                    });

                    const { access, refresh } = response.data;
                    tokenServices.setTokens(access, refresh);

                    origanRequest.headers.Authorization = `Bearer ${access}`;
                    return apiClient.request(origanRequest);
                }
            }catch (refreshError) {
                console.error('Refresh token failed:', refreshError);
                tokenServices.clearTokens();
                window.location.href = '/login';
            }
        }


        return Promise.reject(error);
    }
)
export default apiClient;