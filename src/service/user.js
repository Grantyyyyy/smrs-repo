import axios from "axios";


export const UserService = {
  getMe() {
    const token = localStorage.getItem('access_token');
    return axios.get('http://localhost:8000/api/me/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
  }
};
