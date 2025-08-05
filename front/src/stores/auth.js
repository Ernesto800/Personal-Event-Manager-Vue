import { ref } from 'vue';
import apiClient from '@/api/api';

const TOKEN_KEY = 'jwt_token';

export const isAuthenticated = ref(false);

function initializeAuth() {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token) {
        isAuthenticated.value = true;
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        isAuthenticated.value = false;
        delete apiClient.defaults.headers.common['Authorization'];
    }
}

initializeAuth();

export function setToken(token) {
    if (token) {
        localStorage.setItem(TOKEN_KEY, token);
        isAuthenticated.value = true;
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
}

export function clearToken() {
    localStorage.removeItem(TOKEN_KEY);
    isAuthenticated.value = false;
    delete apiClient.defaults.headers.common['Authorization'];
}