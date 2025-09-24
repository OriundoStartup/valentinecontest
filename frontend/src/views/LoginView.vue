<template>
  <div class="container">
    <h2>Inicio de Sesión (Admin)</h2>
    <form @submit.prevent="submitLogin">
      <div class="form-group">
        <label for="email">Correo Electrónico</label>
        <input type="email" id="email" v-model="form.email" required autocomplete="email">
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input type="password" id="password" v-model="form.password" required autocomplete="current-password">
      </div>
      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
      </button>
      <p v-if="loginError" class="error-message">{{ loginError }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import apiClient from '../utils/axios';

const form = ref({
  email: '',
  password: ''
});

const loginError = ref(null);
const isSubmitting = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const submitLogin = async () => {
  isSubmitting.value = true;
  loginError.value = null;

  try {
    const response = await apiClient.post('token/', {
      username: form.value.email, // <-- Corregido para enviar "username"
      password: form.value.password,
    });
    
    authStore.login(response.data.access);
    router.push({ name: 'dashboard' });

  } catch (error) {
    if (error.response && error.response.status === 401) {
      loginError.value = 'Correo o contraseña incorrectos.';
    } else {
      console.error('Login failed:', error);
      loginError.value = 'Ocurrió un error al intentar iniciar sesión.';
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #1a1a1a;
  color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

h2 {
  color: #ff8c00;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: #fff;
}

input:focus {
  outline: none;
  border-color: #ff8c00;
}

button {
  width: 100%;
  background-color: #ff8c00;
  color: #1a1a1a;
  font-weight: bold;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  background-color: #e57d00;
}

button:disabled {
  background-color: #444;
  cursor: not-allowed;
  color: #888;
}

.error-message {
  color: #dc3545;
  font-size: 0.9em;
  text-align: center;
  margin-top: 10px;
}
</style>