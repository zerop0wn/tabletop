import axios, { AxiosError } from 'axios'

// Use /api proxy when running in browser (works for both local and Docker)
// The Vite proxy will handle routing to the backend
// For production/EC2, you may need to set VITE_API_BASE_URL environment variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('gm_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors - token expired or invalid
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear it and redirect to login
      localStorage.removeItem('gm_token')
      // Only redirect if we're not already on the login page
      if (window.location.pathname !== '/gm/login' && window.location.pathname !== '/gm/login/') {
        window.location.href = '/gm/login'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient

