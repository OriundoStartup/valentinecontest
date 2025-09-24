<template>
  <div class="container">
    <h2>¡El Ganador es!</h2>
    <div v-if="winner">
      <div class="winner-info">
        <p><strong>Nombre:</strong> {{ winner.full_name }}</p>
        <p><strong>Correo:</strong> {{ winner.email }}</p>
      </div>
      <p class="final-message">Se le ha enviado un correo de notificación al ganador.</p>
    </div>
    <div v-else class="no-winner">
      <p>No se ha encontrado información del ganador.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const winner = ref(null)

onMounted(() => {
  const winnerData = new URLSearchParams(window.location.search).get('winnerData')
  if (winnerData) {
    try {
      winner.value = JSON.parse(decodeURIComponent(winnerData))
    } catch (e) {
      console.error('Error al parsear los datos del ganador:', e)
    }
  }
})
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px;
  background-color: #1a1a1a;
  color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  text-align: center;
}

h2 {
  color: #ff8c00;
  font-size: 2em;
  margin-bottom: 20px;
}

.winner-info {
  background-color: #333;
  padding: 20px;
  border-radius: 8px;
  border: 2px solid #ff8c00;
  margin-bottom: 20px;
}

.winner-info p {
  font-size: 1.2em;
  margin: 10px 0;
}

.final-message {
  font-style: italic;
  font-size: 1em;
}

.no-winner {
  color: #dc3545;
  font-weight: bold;
}
</style>