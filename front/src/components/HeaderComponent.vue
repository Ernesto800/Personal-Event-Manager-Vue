<script>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { isAuthenticated, clearToken } from '../stores/auth'; 

export default {
  name: 'HeaderComponent',
  setup() {
    const router = useRouter();
    const route = useRoute();

    const logout = () => {
      clearToken();
      router.push('/login');
    };

    return {
      isAuthenticated,
      logout,
    };
  }
};
</script>

<template>
    <header>
    <nav class="navheader">
      <router-link to="/" class="nav-button">Home</router-link> 
      <router-link to="/events" class="nav-button eventsbutton" v-if="isAuthenticated">Events</router-link>
      <div class="login">
        <router-link to="/login" class="nav-button" v-if="!isAuthenticated">Login</router-link>
        <router-link to="/register" class="nav-button registerbutton" v-if="!isAuthenticated">Registrarse</router-link>
      </div>
      <button class="logout" v-if="isAuthenticated" @click="logout">Logout</button>
    </nav>
  </header>
</template>

<style scoped>
.nav-button, .logout {
  text-decoration: none; 
  display: inline-block;
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-align: center;
  white-space: nowrap;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.1em;
}

.nav-button:hover {
  background-color: #06550a;
}

.eventsbutton {
  background-color: #b0d42f;
}

.registerbutton {
  background-color: #b0d42f;
}

.logout {
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}
.logout:hover {
  background-color: #530b0b;
}

.navheader {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f2f2f2;
  border-bottom: 1px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  gap: 20px;
}
.login {
  display: flex;
  gap: 10px;
  margin-left: auto;
  align-items: center;
  margin-right: 10px;
  gap: 20px;
}

</style>