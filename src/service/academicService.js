import axios from 'axios';
const DEPARTMENT_API_URL = 'http://localhost:8000/api/departments/';
const SUBJECT_API_URL = 'http://localhost:8000/api/subjects/';
const COURSE_API_URL = 'http://localhost:8000/api/courses/';
const SUBJECT_OFFERING_API_URL = 'http://localhost:8000/api/offerings/';
const SCHEDULE_API_URL = 'http://localhost:8000/api/schedules/';

export const Department = {
  getAll() {
    return axios.get(DEPARTMENT_API_URL)
  },

  getConnectedSubjects(deparmentID) {
    return axios.get(`${DEPARTMENT_API_URL}connected_subjects/?department=${deparmentID}`)
  },

  // Fetch a single department by ID
  getOne(id) {
    return axios.get(`${DEPARTMENT_API_URL}${id}/`)
  },

  // Create a new department
  create(data) {
    return axios.post(DEPARTMENT_API_URL, data)
  },

  // Update an existing department
  update(id, data) {
    return axios.put(`${DEPARTMENT_API_URL}${id}/`, data)
  },

  // Delete a department
  delete(id) {
    return axios.delete(`${DEPARTMENT_API_URL}${id}/`)
  }
}
export const Subject = {
  // Fetch all subjects
  getAll() {
    return axios.get(SUBJECT_API_URL)
  },

  // Fetch a single subject by ID
  getOne(id) {
    return axios.get(`${SUBJECT_API_URL}${id}/`)
  },

  // Create a new subject
  create(data) {
    return axios.post(SUBJECT_API_URL, data)
  },

  // Update an existing subject
  update(id, data) {
    return axios.put(`${SUBJECT_API_URL}${id}/`, data)
  },
  
  // Delete a subject
  delete(id) {
    return axios.delete(`${SUBJECT_API_URL}${id}/`)
  }
}
export const Course = {
  // Fetch all courses
  getAll() {
    return axios.get(COURSE_API_URL)
  },

  // Fetch a single course by ID
  getOne(id) {
    return axios.get(`${COURSE_API_URL}${id}/`)
  },

  // Create a new course
  create(data) {
    return axios.post(COURSE_API_URL, data)
  },

  // Update an existing course
  update(id, data) {
    return axios.put(`${COURSE_API_URL}${id}/`, data)
  },
  
  // Delete a course
  delete(id) {
    return axios.delete(`${COURSE_API_URL}${id}/`)
  }
}
export const SubjectOffering = {
  // Fetch all subject offerings
  getBydeparment(deparmentID) {
    return axios.get(`${SUBJECT_OFFERING_API_URL}?department=${deparmentID}`)
  },

  // Fetch a single subject offering by ID
  getOne(id) {
    return axios.get(`${SUBJECT_OFFERING_API_URL}${id}/`)
  },

  // Fetch all schedules for a subject
  getBySubjectOffers(subjectID) {
    return axios.get(`${SUBJECT_OFFERING_API_URL}get_schedules/?subject_offer=${subjectID}`)
  },

  addSchedule(id, data) {
    return axios.post(`${SUBJECT_OFFERING_API_URL}${id}/add_schedule/`, data)
  },

  addInstructor(id, data) {
    return axios.patch(`${SUBJECT_OFFERING_API_URL}${id}/`, data)
  },

  // Create a new subject offering
  create(payload) {
    return axios.post(SUBJECT_OFFERING_API_URL, payload)
  },

  // Update an existing subject offering
  update(id, data) {
    return axios.put(`${SUBJECT_OFFERING_API_URL}${id}/`, data)
  },
  
  // Delete a subject offering
  delete(id) {
    return axios.delete(`${SUBJECT_OFFERING_API_URL}${id}/`)
  } 
}
export const Schedule = {
  getAll() {
    return axios.get(SCHEDULE_API_URL)
  },

  patch(id, data) {
    return axios.patch(`${SCHEDULE_API_URL}${id}/`, data)
  },

  delete(id) {
    return axios.delete(`${SCHEDULE_API_URL}${id}/`)
  }
}
