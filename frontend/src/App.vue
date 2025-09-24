<template>
  <div id="app-container" class="min-h-screen flex flex-col bg-gray-900 text-white">
    <header class="bg-gray-800 shadow-md">
      <nav class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="space-x-4">
          <!-- Enlaces públicos (se muestran si no está autenticado) -->
          <template v-if="!authStore.isAuthenticated">
            <RouterLink to="/" class="hover:text-amber-500 transition-colors">Registro</RouterLink>
            <RouterLink to="/login" class="hover:text-amber-500 transition-colors">Iniciar sesión</RouterLink>
          </template>
          <!-- Enlaces protegidos (se muestran si está autenticado) -->
          <template v-else>
            <RouterLink to="/dashboard" class="hover:text-amber-500 transition-colors">Panel de control</RouterLink>
            <RouterLink to="/winner" class="hover:text-amber-500 transition-colors">Ganador</RouterLink>
            <button @click="authStore.logout" class="hover:text-amber-500 transition-colors">Cerrar sesión</button>
          </template>
        </div>
      </nav>
    </header>

    <main class="flex-grow">
      <div class="container mx-auto px-4 py-6">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { useAuthStore } from './stores/auth';

const authStore = useAuthStore();
</script>

<style>
#app-container {
  display: flex;
  flex-direction: column;
}
</style>
