<script setup>
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore(); // Usar el store de autenticación
const router = useRouter();

const logout = () => {
  authStore.logout(); // Llamar al método logout del store
  alert('Sesión cerrada con éxito');
  router.push('/login'); // Redirigir al inicio de sesión
};
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary sticky-top">
    <div class="container-fluid">
      <RouterLink to="/" class="navbar-brand">Evaluación 4</RouterLink>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <RouterLink to="/" active-class="active" class="nav-link">Home</RouterLink>
          </li>
          <template v-if="authStore.isAuthenticated">
            <li class="nav-item">
              <RouterLink to="/eventos" active-class="active" class="nav-link">Eventos</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/categorias" active-class="active" class="nav-link">Categorías</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/participantes" active-class="active" class="nav-link">Participantes</RouterLink>
            </li>
            <li class="nav-item">
              <button class="btn btn-danger" @click="logout">Cerrar Sesión</button>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <RouterLink to="/register" active-class="active" class="nav-link">Registrarse</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/login" active-class="active" class="nav-link">Iniciar Sesión</RouterLink>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>
