<template>
  <div class="container">
    <h2>Panel de Administración</h2>

    <p v-if="isLoading">Cargando concursantes...</p>
    <p v-else-if="error" class="error-message">{{ error }}</p>

    <div v-else>
      <div class="controls">
        <button @click="performDraw" :disabled="isDrawing || verifiedContestants.length === 0">
          {{ isDrawing ? 'Realizando Sorteo...' : 'Realizar Sorteo' }}
        </button>
      </div>

      <h3>Concursantes Verificados ({{ verifiedContestants.length }})</h3>
      <table class="contestants-table" v-if="verifiedContestants.length > 0">
        <thead>
          <tr>
            <th>Nombre Completo</th>
            <th>Correo Electrónico</th>
            <th>Teléfono</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contestant in verifiedContestants" :key="contestant.email">
            <td>{{ contestant.full_name }}</td>
            <td>{{ contestant.email }}</td>
            <td>{{ contestant.phone }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-contestants">No hay concursantes verificados aún.</p>

      <h3 style="margin-top: 40px;">Todos los Concursantes Registrados ({{ allContestants.length }})</h3>
      <table class="contestants-table" v-if="allContestants.length > 0">
        <thead>
          <tr>
            <th>Nombre Completo</th>
            <th>Correo Electrónico</th>
            <th>Teléfono</th>
            <th>Verificado</th>
            <th>Ganador</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contestant in allContestants" :key="contestant.email">
            <td>{{ contestant.full_name }}</td>
            <td>{{ contestant.email }}</td>
            <td>{{ contestant.phone }}</td>
            <td>{{ contestant.is_verified ? 'Sí' : 'No' }}</td>
            <td>{{ contestant.is_winner ? 'Sí' : 'No' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-contestants">No hay concursantes registrados aún.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../utils/axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const verifiedContestants = ref([])
const allContestants = ref([])
const isLoading = ref(true)
const error = ref(null)
const isDrawing = ref(false)

const router = useRouter()
const authStore = useAuthStore()

const fetchContestants = async () => {
  try {
    const [verifiedRes, allRes] = await Promise.all([
      apiClient.get('contest/verified-contestants/'),
      apiClient.get('contest/contestants/')
    ])
    verifiedContestants.value = verifiedRes.data
    allContestants.value = allRes.data
  } catch (err) {
    if (err.response?.status === 401) {
      authStore.logout()
      router.push({ name: 'login' })
    } else if (err.response?.status === 403) {
      error.value = 'No tienes permisos para ver esta sección.'
    } else {
      error.value = 'No se pudieron cargar los concursantes.'
    }
  } finally {
    isLoading.value = false
  }
}

const performDraw = async () => {
  isDrawing.value = true
  try {
    const response = await apiClient.post('contest/draw-winner/', {})
    router.push({ name: 'winner', query: { winnerData: JSON.stringify(response.data) } })
  } catch (err) {
    alert(err.response?.data?.error || 'Error al realizar el sorteo.')
  } finally {
    isDrawing.value = false
  }
}

onMounted(fetchContestants)
</script>




<style scoped>
.container {
  max-width: 900px;
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

h3 {
  color: #ff8c00;
  margin-top: 30px;
  text-align: center;
}

.controls {
  text-align: center;
  margin-bottom: 20px;
}

button {
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

.contestants-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.contestants-table th,
.contestants-table td {
  border: 1px solid #444;
  padding: 10px;
  text-align: left;
}

.contestants-table th {
  background-color: #333;
}

.no-contestants {
  text-align: center;
  color: #ff8c00;
  font-weight: bold;
  margin-top: 20px;
}

.error-message {
  color: #dc3545;
  text-align: center;
  font-weight: bold;
}
</style>
