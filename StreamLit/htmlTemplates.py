"""
Este script define estilos y plantillas de mensajes para una interfaz similar a un chat.

Incluye:

- Estilos CSS: Definen la apariencia visual de los mensajes del chat tanto para el usuario como para el bot.
- bot_template: Una cadena HTML formateada que representa un mensaje del bot.
- user_template: Una cadena HTML formateada que representa un mensaje del usuario.

Puedes usar estas plantillas dentro de tu aplicación en Streamlit u otro marco web
para crear una interfaz de chat visualmente atractiva e informativa.
"""

css = """
<style>
  /* Docstring para los estilos CSS */
  .chat-message {
    /* Estilos para los contenedores de los mensajes del chat */
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex; /* Permite que los avatares y los mensajes estén uno al lado del otro */
  }

  .chat-message.user {
    /* Estilos para los mensajes del usuario */
    background-color: #2b313e; /* Fondo azul oscuro */
    color: #fff; /* Texto blanco para los mensajes del usuario */
  }

  .chat-message.bot {
    /* Estilos para los mensajes del bot */
    background-color: #475063; /* Fondo azul claro */
    color: #fff; /* Texto blanco para los mensajes del bot */
  }

  .chat-message .avatar {
    /* Estilos para las imágenes de avatar */
    width: 20%; /* Asignar 20% del ancho para los avatares */
  }

  .chat-message .avatar img {
    /* Estilos para las imágenes de avatar dentro de los contenedores de mensajes */
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
  }

  .chat-message .message {
    /* Estilos para el texto del mensaje */
    width: 80%; /* Asignar 80% del ancho para el contenido del mensaje */
    padding: 0 1.5rem; /* Añadir relleno para una mejor legibilidad */
  }
</style>
"""

bot_template = """
<div class="chat-message bot">
  <div class="avatar">
    <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
  <div class="avatar">
    <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

# Mejoras de UI (considera implementarlas en tu aplicación):
# - Permitir a los usuarios personalizar las imágenes de avatar (a través de la carga de archivos o selección)
# - Implementar un campo de entrada de mensajes para la interacción del usuario
# - Integrar las plantillas con el marco elegido para mostrar los mensajes del chat
