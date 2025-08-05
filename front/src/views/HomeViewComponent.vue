<script>
import { computed, ref } from 'vue';
import { isAuthenticated } from '@/stores/auth.js';

export default {
  name: 'HomeViewComponent',
  setup() {
    const username = ref(localStorage.getItem('username') || 'Usuario'); 

    
    return {
      isAuthenticated,
      username
    };
  }
};
</script>

<template>
  <div class="home-container">
    <header class="hero-section">
      <h1 class="hero-title">Tu Vida, Tus Eventos, Organizados.</h1>
      <p class="hero-subtitle">
        Gestiona y planifica tus citas personales y profesionales con facilidad. 
        Nunca más olvides un cumpleaños, una reunión o una tarea importante.
      </p>
      
      <div class="cta-buttons">
        <template v-if="isAuthenticated">
          <p class="welcome-back">¡Bienvenido {{ username }}!</p>
          <router-link to="/events" class="button primary-button">Ir a Mis Eventos</router-link>
        </template>
        
        <template v-else>
          <router-link to="/login" class="button primary-button">Iniciar Sesión</router-link>
          <router-link to="/register" class="button secondary-button">Crear Cuenta</router-link>
        </template>
      </div>
    </header>

    <section class="features-section">
      <h2>Personal Event Manager</h2>
      <div class="feature-grid">
        <div class="feature-item">
          <i class="icon-calendar">🗓️</i> <h3>Organización Sencilla</h3>
          <p>Crea, edita y gestiona tus eventos de forma intuitiva.</p>
        </div>
        <div class="feature-item">
          <i class="icon-notification">🔔</i> <h3>Recordatorios Inteligentes</h3>
          <p>Recibe alertas para que nunca te pierdas nada importante.</p>
        </div>
        <div class="feature-item">
          <i class="icon-security">🔒</i> <h3>Tus Datos Seguros</h3>
          <p>Tu privacidad en serio. Tus eventos están protegidos.</p>
        </div>
      </div>
    </section>

        <footer class="footer">
      <p>&copy; 2025 Personal Event Manager Ernesto Boza</p>
    </footer>
  </div>
</template>


<style scoped>
.home-container {
  font-family: 'Arial', sans-serif;
  color: #333;
  text-align: center;
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  background-color: #eaf7ea;
  padding: 60px 20px;
  border-radius: 12px;
  margin-bottom: 50px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.hero-title {
  font-size: 3.5em;
  color: #2c3e50;
  margin-bottom: 20px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.4em;
  color: #555;
  max-width: 800px;
  margin: 0 auto 30px auto;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.welcome-back {
  font-size: 1.5em;
  color: #4CAF50;
  margin-right: 20px;
  font-weight: bold;
}

.button {
  display: inline-block;
  padding: 15px 30px;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
  transition: all 0.3s ease;
  white-space: nowrap;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.primary-button {
  background-color: #4CAF50;
  color: white;
  border: 2px solid #4CAF50;
  padding-top: 27px;

}

.primary-button:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.secondary-button {
  background-color: white;
  color: #4CAF50;
  border: 2px solid #4CAF50;
}

.secondary-button:hover {
  background-color: #f0fdf0;
  color: #3e8e41;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.features-section {
  padding: 50px 20px;
  background-color: #fff;
  border-radius: 12px;
  margin-bottom: 50px;
}

.features-section h2 {
  font-size: 2.5em;
  color: #2c3e50;
  margin-bottom: 40px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-item {
  background-color: #f9f9f9;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.feature-item i {
  font-size: 3em;
  margin-bottom: 15px;
  color: #4CAF50;
}

.feature-item h3 {
  font-size: 1.5em;
  color: #2c3e50;
  margin-bottom: 10px;
}

.feature-item p {
  font-size: 1.1em;
  color: #666;
}

.footer {
  border-radius: 12px;
}


@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5em;
  }
  .hero-subtitle {
    font-size: 1.2em;
  }
  .cta-buttons {
    flex-direction: column;
    gap: 15px;
  }
  .button {
    width: 80%;
    max-width: 300px;
  }
  .features-section h2, .call-to-action-bottom h2 {
    font-size: 2em;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2em;
  }
  .hero-subtitle {
    font-size: 1em;
  }
  .button {
    width: 90%;
  }
}
</style>