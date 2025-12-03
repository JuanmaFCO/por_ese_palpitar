Por Ese Palpitar Eventos - Plataforma Web

Proyecto desarrollado en **Flask + MongoDB** para la gestión de eventos, pedidos y administración de usuarios.  
Incluye seguridad, perfiles diferenciados y panel de administración.

 Funcionalidades principales

•	Seguridad
- **Login seguro** con hashing de contraseñas (`werkzeug.security`).
- **Sesiones** para mantener usuarios logueados.
- **Roles diferenciados**:
  - **Administrador**: acceso al panel completo.
  - **Cliente**: acceso a su perfil y pedidos.
- **Logout** que limpia la sesión y redirige al login.

•	Perfiles de usuario
- Cada cliente tiene un **perfil personal** con:
  - Nombre
  - Email
  - Rol
- El administrador puede **editar y eliminar usuarios** desde el panel.


•	Panel de administración
- Vista centralizada de todos los usuarios.
- **Crear nuevos usuarios** con rol asignado.
- **Editar datos** de usuarios existentes.
- **Eliminar usuarios** con confirmación.
- Tabla con información detallada y lista rápida estilo minimalista.

•	Pedidos
- Formulario para que clientes envíen pedidos con:
  - Nombre, teléfono, dirección
  - Items solicitados
  - Notas adicionales
- **Confirmación automática** al enviar pedido.
- **Envío de correo SMTP** al administrador con los detalles.

•	Galería multimedia
- Secciones de **fotos y videos** organizadas por categorías:
  - Cumpleaños
  - Infantil
  - Catering
  - Ambientación
- Cada categoría muestra imágenes y videos relacionados.


•	Integración con WhatsApp
- Número de contacto global (`BUSINESS_WHATSAPP`) disponible en todas las páginas.
- Botón directo para comunicación rápida.

•	Tecnologías utilizadas
- **Flask** (framework web en Python)
- **MongoDB** (base de datos NoSQL)
- **Bootstrap 5** (estilo y diseño responsivo)
- **Werkzeug** (seguridad de contraseñas)
- **SMTP** (envío de correos)
- **Jinja2** (templates dinámicos)
