//API client frontend

import axios from 'axios'

export const apiClient = axios.create({
    baseURL: './api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor 
// dove il frontend puo ricevere cio´ che e´esposto dal fastapi nel backend

// Request interceptor (optional - for adding auth tokens later)
apiClient.interceptors.request.use(
  (config) => {
    // You can add authentication tokens here later
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor (optional - for error handling)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data)
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message)
    } else {
      // Something else went wrong
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)