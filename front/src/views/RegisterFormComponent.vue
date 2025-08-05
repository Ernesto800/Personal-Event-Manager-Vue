<script>
import apiClient from '@/api/api';
import { useRouter } from 'vue-router';
import { setToken } from '../stores/auth';

export default {
  name: 'RegisterFormComponent', 
  data() {
    return {
      name: '',
      lastname: '',
      email: '',
      phone: '',
      username: '',
      password: '',
      confirmPassword: '',
      message: '',
      isError: false,
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async register() {
      this.message = '';
      this.isError = false;

      if (this.password !== this.confirmPassword) {
        this.message = 'Las contraseñas no coinciden.';
        this.isError = true;
        return;
      }

      try {
        const response = await apiClient.post('/auth/register', {
          name: this.name,
          lastname: this.lastname,
          email: this.email,
          phone: this.phone,
          username: this.username,
          password: this.password,
        });
        
        setToken(response.data.token);
        if (response.data.username) {
          localStorage.setItem('username', response.data.username);
        }

        this.message = response.data.message + '. ¡Redirigiendo a tus eventos!';
        this.isError = false;
        
        this.router.push('/events'); 
        
      } catch (error) {
        this.isError = true;
        if (error.response) {
          this.message = error.response.data.message || 'Error al registrar usuario.';
        } else if (error.request) {
          this.message = 'No se pudo conectar al servidor. Asegúrate de que el backend esté funcionando.';
        } else {
          this.message = 'Error desconocido al procesar la solicitud.';
        }
        console.error('Error de registro:', error);
      }
    },
  },
};
</script>


<template>
  <form @submit.prevent="register">
    <h2>Registrarse</h2>
    <div>
      <label for="reg-name">Nombre:</label>
      <input type="text" id="reg-name" v-model="name" required />
      <label for="reg-lastname">Apellidos:</label>
      <input type="text" id="reg-lastname" v-model="lastname" required />
      <label for="reg-email">Email:</label>
      <input type="email" id="reg-email" v-model="email" required />
      <label for="reg-phone">Teléfono:</label>
      <input type="tel" id="reg-phone" v-model="phone" required />
    </div>
    <div>
      <label for="reg-username">Nombre de usuario</label>
      <input type="text" id="reg-username" v-model="username" required />
    </div>
    <div>
      <label for="reg-password">Contraseña:</label>
      <input type="password" id="reg-password" v-model="password" required />
      <label for="reg-password-confirm">Confirmar Contraseña:</label>
      <input type="password" id="reg-password-confirm" v-model="confirmPassword" required />
    </div>
    <button type="submit">Registrarme</button>
    <p v-if="message" :class="{ 'error-message': isError, 'success-message': !isError }">{{ message }}</p>
    <p>¿Ya tienes cuenta? <router-link to="/login">Inicia Sesión aquí</router-link></p>
  </form>
</template>


<style scoped>
form {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
}
div {
  display: flex;
  flex-direction: column;
}
label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}
input[type="text"],
input[type="password"],
input[type="email"],
input[type="tel"] {
  width: calc(100% - 22px);
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}
button {
  padding: 10px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #218838;
}
p {
  text-align: center;
}
</style>