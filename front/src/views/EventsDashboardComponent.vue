<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { clearToken, isAuthenticated } from '../stores/auth';
import apiClient from '@/api/api';

export default {
  name: 'EventsDashboardComponent',
  setup() {
    const router = useRouter();
    const events = ref([]);
    const selectedDate = ref(null);
    const isEventModalOpen = ref(false); 
    const currentEvent = ref({
      title: '',
      description: '',
      date: new Date().toISOString().split('T')[0],
      time: '09:00',
    });
    const isEditMode = ref(false);
    const modalMessage = ref('');
    const isModalError = ref(false);

    const eventsForSelectedDate = computed(() => {
      if (!selectedDate.value) return [];
      const dateString = new Date(selectedDate.value).toISOString().split('T')[0];
      return events.value.filter(event => event.date === dateString);
    });

    const sortedEvents = computed(() => {
      return [...events.value].sort((a, b) => new Date(b.date) - new Date(a.date));
    });

    const calendarAttributes = computed(() => [
      ...events.value.map(event => ({
        key: event.id,
        dot: {
          color: 'green',
          class: 'event-dot',
        },
        dates: event.date,
        popover: {
          label: event.title,
        },
      })),
      {
        key: 'selected',
        highlight: {
          color: 'blue',
          fillMode: 'outline',
          class: 'selected-day-highlight',
        },
        dates: selectedDate.value,
      }
    ]);

    const logout = () => {
      clearToken();
      router.push('/login');
    };

    const fetchEvents = async () => {
      if (!isAuthenticated.value) {
        console.log('No autenticado, no se cargarán eventos.');
        return;
      }

      try {
        const response = await apiClient.get('/events');
        events.value = response.data.events;
        console.log('Eventos cargados:', events.value);
      } catch (error) {
        console.error('Error al cargar eventos:', error);
        if (error.response && error.response.status === 401) {
          console.log('Token inválido o expirado, redirigiendo a login.');
          clearToken();
          router.push('/login');
        }
      }
    };

    const openEventModal = (mode, event = null) => {
      isEventModalOpen.value = true;
      modalMessage.value = '';
      isModalError.value = false;

      if (mode === 'new') {
        isEditMode.value = false;
        currentEvent.value = {
          id: null,
          title: '',
          description: '',
          date: selectedDate.value ? new Date(selectedDate.value).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
          time: '09:00',
        };
      } else if (mode === 'edit' && event) {
        isEditMode.value = true;
        currentEvent.value = { ...event };
      }
    };

    const closeEventModal = () => {
      isEventModalOpen.value = false;
      modalMessage.value = '';
      isModalError.value = false;
    };

    const saveEvent = async () => {
      modalMessage.value = '';
      isModalError.value = false;
      try {
        if (isEditMode.value) {
          await apiClient.put(`/events/${currentEvent.value.id}`, currentEvent.value);
          modalMessage.value = 'Evento actualizado con éxito!';
        } else {
          await apiClient.post('/events', currentEvent.value);
          modalMessage.value = 'Evento creado con éxito!';
        }
        await fetchEvents();
        setTimeout(() => closeEventModal(), 1500);
      } catch (error) {
        isModalError.value = true;
        modalMessage.value = error.response?.data?.message || 'Error al guardar el evento.';
        console.error('Error al guardar evento:', error);
      }
    };

     const deleteEvent = async (eventIdToDelete) => {
      modalMessage.value = '';
      isModalError.value = false;
      try {
        const response = await apiClient.delete(`/events/${eventIdToDelete}`);
        modalMessage.value = 'Evento eliminado con éxito!';
        await fetchEvents();
        closeEventModal();
      } catch (error) {
        isModalError.value = true;
        modalMessage.value = error.response?.data?.message || 'Error al eliminar el evento.';
        console.error('ERROR: Error al eliminar evento:', error.response?.data || error.message);
      }
    };

    const onDayClick = (day) => {
      selectedDate.value = day.date;
    };

    const selectEvent = (event) => {
      openEventModal('edit', event);
    };

    const formatDate = (dateString) => {
      const options = { month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    };
    const formatFullDate = (date) => {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('es-ES', options);
    };

    onMounted(() => {
      if (isAuthenticated.value) {
        fetchEvents();
      }
    });

    watch(isAuthenticated, (newValue) => {
      if (newValue) {
        fetchEvents();
      } else {
        events.value = [];
      }
    });


    return {
      logout,
      events,
      selectedDate,
      eventsForSelectedDate,
      sortedEvents,
      calendarAttributes,
      isEventModalOpen,
      currentEvent,
      isEditMode,
      modalMessage,
      isModalError,
      openEventModal,
      closeEventModal,
      saveEvent,
      deleteEvent,
      onDayClick,
      selectEvent,
      formatDate,
      formatFullDate,
    };
  }
};
</script>


<template>
  <div class="events-dashboard">
    <header class="dashboard-header">
      <h1>Panel de Eventos</h1>
    </header>

    <div class="main-content">
      <aside class="sidebar">
        <h2>Mis Eventos Recientes</h2>
        <ul v-if="events.length">
          <li v-for="event in sortedEvents" :key="event.id" class="event-item" @click="selectEvent(event)">
            <div class="event-info" @click="selectEvent(event)">
              <div class="event-date">{{ formatDate(event.date) }}</div>
              <div class="event-title">{{ event.title }}</div>
              <div class="event-description">{{ event.description }}</div>
            </div>
            <button class="button-trash" @click.stop="deleteEvent(event.id)">
              <img src="/public/recycle-bin.png" alt="Eliminar" class="img-trash">
            </button>
          </li>
        </ul>
        <p v-else>No tienes eventos registrados aún.</p>

        <button @click="openEventModal('new')" class="add-event-button">
          + Añadir Nuevo Evento
        </button>
      </aside>

      <section class="calendar-section">
        <VCalendar
          class="custom-calendar"
          :attributes="calendarAttributes"
          is-expanded
          @dayclick="onDayClick"
        />
        <p class="selected-date-info" v-if="selectedDate">
          Eventos para: {{ formatFullDate(selectedDate) }}
        </p>
        <div class="events-for-day" v-if="eventsForSelectedDate.length">
          <h3>Eventos del día:</h3>
          <ul>
            <li v-for="event in eventsForSelectedDate" :key="event.id" class="day-event-item" @click="selectEvent(event)">
              <strong>{{ event.title }}</strong> - {{ event.description }} ({{ event.time }})
            </li>
          </ul>
        </div>
        <p v-else-if="selectedDate">No hay eventos para este día.</p>
      </section>
    </div>

    <div v-if="isEventModalOpen" class="modal-overlay" @click.self="closeEventModal">
      <div class="modal-content">
        <h2>{{ isEditMode ? 'Editar Evento' : 'Añadir Nuevo Evento' }}</h2>
        <form @submit.prevent="saveEvent">
          <div class="form-group">
            <label for="eventTitle">Título:</label>
            <input type="text" id="eventTitle" v-model="currentEvent.title" required />
          </div>
          <div class="form-group">
            <label for="eventDescription">Descripción:</label>
            <textarea id="eventDescription" v-model="currentEvent.description"></textarea>
          </div>
          <div class="form-group">
            <label for="eventDate">Fecha:</label>
            <VDatePicker v-model="currentEvent.date" :model-config="{ type: 'string', mask: 'YYYY-MM-DD' }"/>
          </div>
          <div class="form-group">
            <label for="eventTime">Hora:</label>
            <input type="time" id="eventTime" v-model="currentEvent.time" />
          </div>
          
          <div class="modal-buttons">
            <button type="submit" class="button primary-button">{{ isEditMode ? 'Guardar Cambios' : 'Crear Evento' }}</button>
            <button type="button" @click="closeEventModal" class="button secondary-button">Cancelar</button>
          </div>
        </form>
        <p v-if="modalMessage" :class="{ 'success-message': !isModalError, 'error-message': isModalError }">{{ modalMessage }}</p>
      </div>
    </div>
  </div>
</template>



<style scoped>
.events-dashboard {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 60px);
  padding: 20px;
  background-color: #f7f9fc;
  font-family: 'Arial', sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.dashboard-header h1 {
  color: #2c3e50;
  font-size: 2.5em;
  margin: 0;
}

.logout-button {
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.main-content {
  display: flex;
  flex-grow: 1;
  gap: 30px;
}

.sidebar {
  flex: 0 0 600px;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.sidebar h2 {
  color: #333;
  font-size: 1.8em;
  margin-top: 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
  overflow-y: auto;
}

.event-item {
  background-color: #639666;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 3px;
  padding: 12px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.event-item:last-child {
  border-bottom: none;
}

.event-item:hover {
  background-color: #398155;
}

.button-trash{
  background-color: transparent;
  border: none;
  width: 25px;
  height: 25px;
}

.img-trash{
  background-color: transparent;
  border: none;
  border-radius: 5px;
  width: 25px;
  height: 25px;
}

.img-trash:hover{
  background-color: #2db15f;
  border: none;
  width: 25px;
  height: 25px;
  cursor: pointer;
}

.event-date {
  font-weight: bold;
  color: #555;
  width: 80px;
  flex-shrink: 0;
}

.event-title {
  flex-grow: 1;
  text-align: left;
  margin-top: 10px;
  margin-left: 10px;
  color: #444;
}

.event-description{
  flex-grow: 1;
  text-align: left;
  margin-top: 7px;
  margin-left: 10px;
  color: #646262;
}

.add-event-button {
  background-color: #4CAF50;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  margin-top: 20px;
  transition: background-color 0.3s ease;
  width: 100%;
}

.add-event-button:hover {
  background-color: #306e33;
}

.calendar-section {
  flex-grow: 1;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.custom-calendar {
  width: 100%;
  border: none;
}

:deep(.vc-dots span.event-dot) {
  background-color: #4CAF50;
  width: 7px;
  height: 7px;
}

:deep(.vc-highlight.selected-day-highlight) {
  border: 2px solid #007bff;
  background-color: rgba(0, 123, 255, 0.1);
}

.selected-date-info {
  margin-top: 20px;
  font-size: 1.2em;
  color: #555;
  font-weight: bold;
}

.events-for-day h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #333;
  font-size: 1.5em;
}

.events-for-day ul {
  list-style: none;
  padding: 0;
}

.day-event-item {
  background-color: #e6f7ff;
  border-left: 5px solid #007bff;
  padding: 10px 15px;
  margin-bottom: 8px;
  border-radius: 4px;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.day-event-item:hover {
  background-color: #d9edf7;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  position: relative;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { transform: translateY(-30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 25px;
  color: #2c3e50;
  font-size: 2em;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input[type="text"],
.form-group input[type="time"],
.form-group textarea,
.form-group .vc-container { 
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-group input[type="text"],
.form-group input[type="time"],
.form-group textarea {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
}

.button {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.primary-button {
  background-color: #007bff;
  color: white;
}
.primary-button:hover {
  background-color: #0056b3;
  transform: translateY(-1px);
}

.secondary-button {
  background-color: #6c757d;
  color: white;
}
.secondary-button:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
}

.delete-button {
  background-color: #dc3545;
  color: white;
}
.delete-button:hover {
  background-color: #c82333;
  transform: translateY(-1px);
}

.success-message {
  color: green;
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
}
.error-message {
  color: red;
  margin-top: 15px;
  text-align: center;
  font-weight: bold;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  .sidebar {
    flex: none;
    width: 100%;
    margin-bottom: 30px;
  }
  .modal-content {
    padding: 20px;
  }
  .dashboard-header h1 {
    font-size: 2em;
  }
  .modal-buttons {
    flex-direction: column;
    align-items: center;
  }
  .modal-buttons .button {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>