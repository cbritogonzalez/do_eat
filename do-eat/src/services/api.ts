import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:3000', // Updated this to point to our backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor (useful for adding auth tokens)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const createProfile = async (profileData: any) => {
  console.log('createProfile called with:', profileData); // Add this line
  try {
    const response = await api.post('/saveProfile', profileData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;