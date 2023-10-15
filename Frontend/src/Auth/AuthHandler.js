import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Replace with your API base URL

export const register = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/register`, {
      username: username,
      password: password,
    });
    console.log(response.data)

    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, {
      username,
      password,
    });
    
    const { token } = response.data;
    // Store the token in a cookie named 'token'
    document.cookie = `token=${token}`;

    return true
  } catch (error) {
    throw error.response.data;
  }
};

export const logout = async () => {
  try {
    // Clear the 'token' cookie to log out the user
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    await axios.get(`${API_BASE_URL}/logout`);
    
  } catch (error) {
    throw error.response.data;
  }
};
