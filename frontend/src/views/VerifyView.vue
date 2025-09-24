<template>
  <div class="container">
    <h2>Verificación de Cuenta</h2>

    <p v-if="statusMessage" class="status-message">{{ statusMessage }}</p>

    <form @submit.prevent="submitPassword" v-if="!isVerified">
      <div class="form-group">
        <label for="password">Crea tu Contraseña</label>
        <input type="password" id="password" v-model="password" required autocomplete="new-password" />
      </div>

      <div class="form-group">
        <label for="confirm_password">Confirma tu Contraseña</label>
        <input type="password" id="confirm_password" v-model="confirmPassword" required autocomplete="new-password" />
      </div>

      <p v-if="error" class="error-message">{{ error }}</p>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Verificando...' : 'Verificar Cuenta' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const password = ref('')
const confirmPassword = ref('')
const statusMessage = ref(null)
const isVerified = ref(false)
const isSubmitting = ref(false)
const error = ref(null)
const token = ref('')

onMounted(() => {
  token.value = route.params.token || route.query.token
})

const submitPassword = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = 'Las contraseñas no coinciden.'
    return
  }

  isSubmitting.value = true
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/verify-account/', {
      token: token.value,
      password: password.value
    })

    isVerified.value = true
    statusMessage.value = response.data.message || 'Cuenta verificada correctamente.'
    setTimeout(() => router.push({ name: 'register' }), 4000)
  } catch (err) {
    error.value = err.response?.data?.error || 'Error al verificar la cuenta.'
  } finally {
    isSubmitting.value = false
  }
}
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

.status-message {
  color: #16a34a;
  font-size: 0.95em;
  text-align: center;
  margin-bottom: 15px;
}

.error-message {
  color: #dc3545;
  font-size: 0.9em;
  text-align: center;
  margin-top: 10px;
}
</style>
