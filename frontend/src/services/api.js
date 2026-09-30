import axios from 'axios';

// API Base URL - Flask backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Auth APIs
export const authAPI = {
  login: (identifier, password) => {
    const formData = new FormData();
    formData.append('identifier', identifier);
    formData.append('password', password);
    return axios.post(`${API_BASE_URL}/login`, formData, { withCredentials: true });
  },

  logout: () => {
    return api.get('/logout');
  },

  getCurrentUser: () => {
    return api.get('/api/auth/current-user');
  },

  changePassword: (currentPassword, newPassword, confirmPassword) => {
    const formData = new FormData();
    formData.append('current_password', currentPassword);
    formData.append('new_password', newPassword);
    formData.append('confirm_password', confirmPassword);
    return axios.post(`${API_BASE_URL}/change-password`, formData, { 
      withCredentials: true 
    });
  }
};

// Dashboard APIs
export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard-stats'),
  getDashboard: () => api.get('/dashboard')
};

// Student APIs
export const studentAPI = {
  getAll: (search = '', deptId = null, year = null, gender = '', status = '') => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (deptId) params.append('department_id', deptId);
    if (year) params.append('year', year);
    if (gender) params.append('gender', gender);
    if (status) params.append('status', status);
    return api.get(`/students/?${params.toString()}`);
  },

  getById: (id) => api.get(`/students/${id}`),

  create: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });
    return axios.post(`${API_BASE_URL}/students/add`, formData, { 
      withCredentials: true 
    });
  },

  update: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });
    return axios.post(`${API_BASE_URL}/students/${id}/edit`, formData, { 
      withCredentials: true 
    });
  },

  delete: (id) => {
    const formData = new FormData();
    return axios.post(`${API_BASE_URL}/students/${id}/delete`, formData, { 
      withCredentials: true 
    });
  }
};

// Attendance APIs
export const attendanceAPI = {
  getAll: (date = null, deptId = null, subjectId = null) => {
    const params = new URLSearchParams();
    if (date) params.append('date', date);
    if (deptId) params.append('department_id', deptId);
    if (subjectId) params.append('subject_id', subjectId);
    return api.get(`/attendance/?${params.toString()}`);
  },

  mark: (attendanceData) => {
    const formData = new FormData();
    Object.keys(attendanceData).forEach(key => {
      formData.append(key, attendanceData[key]);
    });
    return axios.post(`${API_BASE_URL}/attendance/mark`, formData, { 
      withCredentials: true 
    });
  },

  getLowAttendance: () => api.get('/attendance/low-attendance'),

  getReport: () => api.get('/attendance/report'),

  delete: (id) => {
    const formData = new FormData();
    return axios.post(`${API_BASE_URL}/attendance/delete/${id}`, formData, { 
      withCredentials: true 
    });
  }
};

// Marks APIs
export const marksAPI = {
  getAll: (search = '', examName = '', subjectId = null, semester = null, status = '') => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (examName) params.append('exam_name', examName);
    if (subjectId) params.append('subject_id', subjectId);
    if (semester) params.append('semester', semester);
    if (status) params.append('status', status);
    return api.get(`/marks/?${params.toString()}`);
  },

  add: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });
    return axios.post(`${API_BASE_URL}/marks/add`, formData, { 
      withCredentials: true 
    });
  },

  edit: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });
    return axios.post(`${API_BASE_URL}/marks/edit/${id}`, formData, { 
      withCredentials: true 
    });
  },

  delete: (id) => {
    const formData = new FormData();
    return axios.post(`${API_BASE_URL}/marks/delete/${id}`, formData, { 
      withCredentials: true 
    });
  },

  getMarksheet: (studentId) => api.get(`/marks/marksheet/${studentId}`)
};

// Fees APIs
export const feesAPI = {
  getAll: (search = '', status = '') => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (status) params.append('status', status);
    return api.get(`/fees/?${params.toString()}`);
  },

  add: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });
    return axios.post(`${API_BASE_URL}/fees/add`, formData, { 
      withCredentials: true 
    });
  },

  pay: (feeId, data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });
    return axios.post(`${API_BASE_URL}/fees/pay/${feeId}`, formData, { 
      withCredentials: true 
    });
  },

  getReceipt: (paymentId) => api.get(`/fees/receipt/${paymentId}`),

  getStudentLedger: (studentId) => api.get(`/fees/student/${studentId}`),

  delete: (feeId) => {
    const formData = new FormData();
    return axios.post(`${API_BASE_URL}/fees/delete/${feeId}`, formData, { 
      withCredentials: true 
    });
  }
};

// Timetable APIs
export const timetableAPI = {
  getAll: () => api.get('/timetable/'),

  manage: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(key => {
      formData.append(key, data[key]);
    });
    return axios.post(`${API_BASE_URL}/timetable/manage`, formData, { 
      withCredentials: true 
    });
  },

  delete: (id) => {
    const formData = new FormData();
    return axios.post(`${API_BASE_URL}/timetable/delete/${id}`, formData, { 
      withCredentials: true 
    });
  }
};

// Report APIs
export const reportAPI = {
  getIndex: () => api.get('/reports/'),
  getStudentReport: () => api.get('/reports/students'),
  getAttendanceReport: () => api.get('/reports/attendance'),
  getMarksReport: () => api.get('/reports/marks'),
  getFeeReport: () => api.get('/reports/fees'),
  getTimetableReport: () => api.get('/reports/timetable')
};

// Generic data APIs (Departments, Subjects, etc.)
export const dataAPI = {
  getDepartments: () => api.get('/api/departments'),
  getSubjects: () => api.get('/api/subjects'),
  getActiveStudents: () => api.get('/api/active-students')
};

export default api;
