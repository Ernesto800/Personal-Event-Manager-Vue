<script>
import apiClient from '@/api/api';
import { useRouter } from 'vue-router';
import { setToken } from '../stores/auth';

export default {
  name: 'LoginFormComponent',
  data() {
    return {
      username: '',
      password: '',
      message: '',
      isError: false,
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async login() {
      this.message = '';
      this.isError = false;
      try {
        const response = await apiClient.post('/auth/login', {
          username: this.username,
          password: this.password,
        });
        this.message = response.data.message;
        
        setToken(response.data.token);
        
        if (response.data.username) {
          localStorage.setItem('username', response.data.username);
        }

        this.isError = false;
        this.router.push('/events'); 

      } catch (error) {
        this.isError = true;
        if (error.response) {
          this.message = error.response.data.message || 'Error al iniciar sesión.';
        } else {
          this.message = 'Error de red o servidor no disponible.';
        }
        console.error('Error de login:', error);
      }
    },
  },
};
</script>


<template>
  <div class="form-container">
    <form @submit.prevent="login" class="form-card">
      <h2>Iniciar Sesión</h2>
      <div class="form-group">
        <label for="username">Usuario:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Iniciar Sesión</button>
      <p v-if="message" :class="{ 'error-message': isError, 'success-message': !isError }">{{ message }}</p>
      <p class="router-link-text">¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link></p>
    </form>
  </div>
</template>


<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px);
  background-color: #f0f2f5;
  padding: 20px;
}

.form-card {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: #ffffff;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
}

h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
  font-size: 2em;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  margin-bottom: 8px;
  color: #555;
}

input[type="text"],
input[type="password"] {
  width: calc(100% - 24px);
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1.05em;
  box-sizing: border-box;
}

button[type="submit"] {
  width: 100%;
  padding: 12px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.15em;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin-top: 15px;
}

button[type="submit"]:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

p {
  text-align: center;
  margin-top: 15px;
}

.error-message {
  color: #d32f2f;
  font-weight: bold;
}

.success-message {
  color: #4CAF50;
  font-weight: bold;
}

.router-link-text a {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.router-link-text a:hover {
  text-decoration: underline;
}
</style>