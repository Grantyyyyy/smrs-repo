import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000/api/departments/';

export const Department = {
  // Fetch all departments
  getAll() {
    return axios.get(API_BASE_URL)
  },

  // Fetch a single department by ID
  getOne(id) {
    return axios.get(`${API_BASE_URL}${id}/`)
  },

  // Create a new department
  create(data) {
    return axios.post(API_BASE_URL, data)
  },

  // Update an existing department
  update(id, data) {
    return axios.put(`${API_BASE_URL}${id}/`, data)
  },

  // Delete a department
  delete(id) {
    return axios.delete(`${API_BASE_URL}${id}/`)
  }
}