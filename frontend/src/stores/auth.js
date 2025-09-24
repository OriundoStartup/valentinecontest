import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false);

  // Acción para inicializar el estado de autenticación al cargar la tienda
  const initializeAuth = () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      isAuthenticated.value = true;
    }
  };

  const login = (token) => {
    localStorage.setItem('access_token', token);
    isAuthenticated.value = true;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    isAuthenticated.value = false;
  };

  // Llama a la inicialización de forma automática
  // Esto asegura que la tienda cargue el estado de autenticación de inmediato
  initializeAuth();

  return {
    isAuthenticated,
    login,
    logout,
  };
});
