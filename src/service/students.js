import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000/api/students/';
const APPROVAL_URL = 'http://localhost:8000/api/users/';

export const Student = {

  getAll() {
    return axios.get(API_BASE_URL)
  },


  getOne(id) {
    return axios.get(`${API_BASE_URL}${id}/`)
  },


  create(data) {
    return axios.post(API_BASE_URL, data)
  },


  update(id, data) {
    return axios.put(`${API_BASE_URL}${id}/`, data)
  },

  approve(id, data) {
    return axios.post(`${APPROVAL_URL}${id}/approve_student/`, data)
  },


  delete(id) {
    return axios.delete(`${API_BASE_URL}${id}/`)
  }
}

