# Personal Event Manager
Este es un gestor de eventos personal que te permite organizar y seguir tus eventos importantes. La aplicación consta de un frontend desarrollado con Vue.js y un backend construido con Flask, utilizando una base de datos SQLite.

## Características
Autenticación de Usuarios: Registro y inicio de sesión seguro para gestionar tus eventos.

Gestión de Eventos:

Crear nuevos eventos con título, descripción, fecha y hora.

Ver todos tus eventos en una lista y en un calendario.

Editar eventos existentes.

Eliminar eventos.

Interfaz Intuitiva: Un panel de control amigable con un calendario interactivo.

Tecnologías Utilizadas
### Frontend
Vue.js 3: Framework progresivo para la interfaz de usuario.

Vue Router 4: Para la navegación entre vistas.

Axios: Cliente HTTP para realizar solicitudes al backend.

V-Calendar: Componente de calendario para Vue.js.

CSS: Estilos personalizados.

Vite: Herramienta de construcción rápida para el desarrollo.

### Backend
Flask: Microframework web para Python.

Flask-SQLAlchemy: Extensión de Flask para interactuar con bases de datos usando SQLAlchemy ORM.

Flask-JWT-Extended: Para la autenticación basada en JSON Web Tokens (JWT).

Flask-Migrate: Para manejar las migraciones de la base de datos (actualizaciones del esquema).

Flask-CORS: Para manejar las políticas de Cross-Origin Resource Sharing.

Werkzeug: Utilizado para el hashing de contraseñas.

python-dotenv: Para cargar variables de entorno desde un archivo .env.

Base de Datos
SQLite: Base de datos ligera basada en archivos, ideal para desarrollo.

Configuración del Entorno de Desarrollo
Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

Prerrequisitos
Python

Node.js y npm (o yarn)

Git


1. Iniciar el Backend (Terminal 1)
Abre una nueva terminal.

Navega a la carpeta back/.

Activa tu entorno virtual.

Asegúrate de que FLASK_APP esté configurado

Inicia el servidor Flask:

python run.py

El backend se ejecutará en http://127.0.0.1:5000.

2. Iniciar el Frontend (Terminal 2)
Abre otra nueva terminal.

Navega a la carpeta front/.

Inicia el servidor de desarrollo de Vue:

npm run dev
o yarn dev

El frontend se ejecutará en http://localhost:5173.

3. Acceder a la Aplicación
Abre tu navegador web y ve a http://localhost:5173.

Uso de la Aplicación
Registro: Al iniciar la aplicación por primera vez, deberás registrar una nueva cuenta. Asegúrate de usar un nombre de usuario y un correo electrónico únicos.

Inicio de Sesión: Después de registrarte, o si ya tienes una cuenta, puedes iniciar sesión con tus credenciales.

Panel de Eventos: Una vez autenticado, serás redirigido al panel de eventos, donde podrás:

Ver tus eventos recientes en la barra lateral.

Ver y añadir eventos en el calendario.

Hacer clic en un evento en la lista o en el calendario para editarlo.

Hacer clic en el icono de la papelera junto a un evento en la lista para eliminarlo directamente.

Añadir nuevos eventos usando el botón "Añadir Nuevo Evento".
