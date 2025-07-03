import axios from 'axios';




const API_BASE_URL = 'http://localhost:8000/api/login/';



export const LoginService = {

    async login(data) {
        try {
            const response = await axios.post(API_BASE_URL, data);
            

            const { access, refresh, user_type, user } = response.data;


            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);


            localStorage.setItem('user_type', user_type || user?.user_type);
            localStorage.setItem('user_id', user?.id);
            localStorage.setItem('username', user?.username);

            return user_type || user?.user_type;
        } catch (error) {
            if (error.response && error.response.data) {
                console.error('Login failed:', error.response.data);
            } else {
                console.error('Login failed:', error.message);
            }

            throw error;
        }
    },

    async logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_type');
        localStorage.removeItem('user_id');
        localStorage.removeItem('username');

        return axios.post(`${API_BASE_URL}logout/`);
    },
}
