<template>
  <div class="container">
    <h2>Inscripción al Concurso</h2>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <form @submit.prevent="submitForm" v-else>
      <div class="form-group">
        <label for="full_name">Nombre Completo</label>
        <input type="text" id="full_name" v-model="form.full_name" required />
      </div>

      <div class="form-group">
        <label for="email">Correo Electrónico</label>
        <input type="email" id="email" v-model="form.email" required />
        <p v-if="emailError" class="error-message">{{ emailError }}</p>
      </div>

      <div class="form-group">
        <label for="phone">Teléfono</label>
        <input type="tel" id="phone" v-model="form.phone" />
      </div>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Inscribiendo...' : 'Inscribirme' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({ full_name: '', email: '', phone: '' })
const successMessage = ref(null)
const emailError = ref(null)
const isSubmitting = ref(false)

const submitForm = async () => {
  isSubmitting.value = true
  try {
    await axios.post('http://127.0.0.1:8000/api/contestants/', form.value)
    successMessage.value = '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.'
    emailError.value = null
  } catch (error) {
    if (error.response?.data?.email) {
      emailError.value = 'El correo electrónico ya está registrado.'
    } else {
      alert('Error al registrarse. Intenta de nuevo.')
    }
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

.success-message {
  color: #16a34a;
  font-size: 0.95em;
  text-align: center;
  margin-bottom: 15px;
}

.error-message {
  color: #dc3545;
  font-size: 0.9em;
  margin-top: 5px;
}
</style>
