// src/api/authApi.ts
import axiosClient from './axiosClient';

// Gom tất cả các tính năng liên quan đến Xác thực (Authentication) vào một object
export const loginApi = {
  login: (username: string, password: string) => {

    return axiosClient.post('/login', { 
      username: username, 
      password: password 
    });
  },

  isAuthenticated: () => {
    return localStorage.getItem('isLoggedIn') === 'true';
  },

  logout: () => {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('username');
    

  }
};