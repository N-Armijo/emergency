<script setup>
import { ref, watch, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore'; // Importar authStore
import participantesService from '@/services/participantesService';

const props = defineProps({
  eventos: Array, // Lista de eventos paginada
  currentPage: Number, // Página actual
  totalPages: Number, // Total de páginas
});

const emit = defineEmits(['pageChange', 'verDetalles']);

// Estado local para manejar inscripciones
const estadoEventos = ref({});

// Acceso al authStore
const authStore = useAuthStore();

// Emitir evento para inscribirse
const handleInscribirse = async (id) => {
  console.log(`Intentando inscribirse al evento con ID: ${id}`);
  try {
    // Obtener datos del usuario desde el authStore
    const user = JSON.parse(localStorage.getItem('user')) || {};
    if (!user.username || !user.email) {
      alert('Error: Usuario no autenticado o datos incompletos.');
      console.error('Datos del usuario en authStore:', {
        username: user.username,
        email: user.email,
      });
      return;
    }

    // Preparar el payload para la inscripción
    const payload = {
      nombre: user.username, // Nombre del usuario
      correo: user.email,    // Correo del usuario
      evento: id,            // ID del evento
    };

    // Depuración: Imprimir los campos que se enviarán en el cuerpo de la solicitud
    console.log('Payload enviado al backend:', JSON.stringify(payload, null, 2));

    // Realizar la inscripción
    const response = await participantesService.createParticipante(payload);
    console.log('Inscripción exitosa:', response.data);

    // Actualizar estado local
    estadoEventos.value[id] = response.data.id;
    alert('Te has inscrito en el evento con éxito.');
  } catch (err) {
    console.error('Error al inscribirse en el evento:', {
      status: err.response?.status,
      data: err.response?.data,
      message: err.message,
    });
    alert('No se pudo inscribir en el evento. Verifica los datos e intenta nuevamente.');
  }
};

// Emitir evento para desinscribirse
const handleDesinscribirse = async (eventoId) => {
  console.log(`Intentando desinscribirse del evento con ID: ${eventoId}`);
  try {
    const participanteId = estadoEventos.value[eventoId];
    if (!participanteId) {
      alert('No estás inscrito en este evento.');
      return;
    }

    await participantesService.deleteParticipante(participanteId); // Usar el ID del participante
    console.log(`Desinscripción exitosa del evento con ID: ${eventoId}`);

    // Actualizar estado local
    estadoEventos.value[eventoId] = null;
    alert('Te has desinscrito del evento con éxito.');
  } catch (err) {
    console.error('Error al desinscribirse:', err.response?.data || err.message);
    alert('No se pudo desinscribir del evento. Intenta nuevamente.');
  }
};

// Inicializar estado de eventos
const inicializarEstado = () => {
  props.eventos.forEach((evento) => {
    if (!estadoEventos.value[evento.id]) {
      estadoEventos.value[evento.id] = null; // Inicializar como no inscrito
    }
  });
};

// Sincronizar estado de eventos inscritos desde el backend
const sincronizarEstadoEventos = async () => {
  try {
    const response = await participantesService.getParticipantes();
    const participantes = response.data;

    // Recorrer todos los eventos y asignar estado basado en inscripción
    props.eventos.forEach((evento) => {
      const participante = participantes.find((p) => p.evento === evento.id);
      estadoEventos.value[evento.id] = participante ? participante.id : null; // Guardar ID del participante
    });

    console.log('Estado sincronizado con los participantes:', estadoEventos.value);
  } catch (err) {
    console.error('Error al sincronizar eventos inscritos:', err.response?.data || err.message);
  }
};

// Recalcular estado cuando cambien los eventos
watch(() => props.eventos, () => {
  inicializarEstado();
  sincronizarEstadoEventos();
});

// Inicializar al montar
onMounted(() => {
  inicializarEstado();
  sincronizarEstadoEventos();
});
</script>

<template>
  <div class="col-12 col-md-8 mx-auto">
    <table class="table table-hover text-center table-striped mt-4">
      <thead>
        <tr>
          <th>Título</th>
          <th>Fecha</th>
          <th>Ubicación</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="evento in eventos" :key="evento.id">
          <td>{{ evento.titulo }}</td>
          <td>{{ evento.fecha }}</td>
          <td>{{ evento.ubicacion }}</td>
          <td>
            <!-- Botón de inscribirse -->
            <button
              class="btn btn-primary btn-sm"
              @click="handleInscribirse(evento.id)"
              :disabled="estadoEventos[evento.id] !== null"
            >
              Inscribirse
            </button>

            <!-- Botón de desinscribirse -->
            <button
              class="btn btn-danger btn-sm ms-2"
              @click="handleDesinscribirse(evento.id)"
              :disabled="estadoEventos[evento.id] === null"
            >
              Desinscribirse
            </button>

            <!-- Botón para ver detalles -->
            <button
              class="btn btn-info btn-sm ms-2"
              @click="$emit('verDetalles', evento.id)"
            >
              Ver Detalles
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Paginación -->
    <nav v-if="totalPages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="$emit('pageChange', currentPage - 1)">
            Anterior
          </button>
        </li>
        <li
          class="page-item"
          v-for="page in totalPages"
          :key="page"
          :class="{ active: currentPage === page }"
        >
          <button class="page-link" @click="$emit('pageChange', page)">
            {{ page }}
          </button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="$emit('pageChange', currentPage + 1)">
            Siguiente
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>
