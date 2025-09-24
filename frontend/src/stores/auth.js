import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false);
  const token = ref(null);
  const fullName = ref(null);
  const email = ref(null);

  const initializeAuth = () => {
    const storedToken = localStorage.getItem('access_token');
    const storedName = localStorage.getItem('full_name');
    const storedEmail = localStorage.getItem('email');

    if (storedToken) {
      token.value = storedToken;
      fullName.value = storedName;
      email.value = storedEmail;
      isAuthenticated.value = true;
    }
  };

  const login = (accessToken, userInfo = {}) => {
    token.value = accessToken;
    fullName.value = userInfo.full_name || '';
    email.value = userInfo.email || '';
    isAuthenticated.value = true;

    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('full_name', fullName.value);
    localStorage.setItem('email', email.value);
  };

  const logout = () => {
    token.value = null;
    fullName.value = null;
    email.value = null;
    isAuthenticated.value = false;

    localStorage.removeItem('access_token');
    localStorage.removeItem('full_name');
    localStorage.removeItem('email');
  };

  initializeAuth();

  return {
    isAuthenticated,
    token,
    fullName,
    email,
    login,
    logout,
  };
});
