# 📁 Estructura del Proyecto - Separación de Concerns

Este documento describe la nueva estructura del proyecto con separación de CSS y JavaScript en archivos externos.

---

## 🏗️ Estructura de Carpetas

```
nginx_facultad/
├── css/                          # Estilos CSS (separados por funcionalidad)
│   ├── styles.css               # Estilos globales, variables de marca y componentes comunes
│   └── forms.css                # Estilos específicos de formularios
├── js/                           # Scripts JavaScript (separados por funcionalidad)
│   ├── theme.js                 # Gestor de tema claro/oscuro
│   ├── form-handler.js          # Manejador de envío de formularios
│   └── utils.js                 # Funciones utilitarias globales
├── templates/                    # Plantillas HTML (Jinja2)
│   ├── alumnos.html             # Listado de alumnos
│   ├── formulario_alumnos.html  # Formulario de búsqueda de becados
│   ├── formulario_crear_alumnos.html  # Formulario para crear alumnos (NUEVO)
│   ├── home.html                # Página de inicio con detalle de alumno
│   └── resultado_alumnos.html   # Página de resultados
├── BBDD/                        # Módulos de base de datos
├── docs/                        # Documentación del proyecto
├── html/                        # Archivos HTML estáticos (respaldo)
├── docker-compose.yml           # Orquestación de contenedores
├── Dockerfile                   # Construcción de imagen
├── main_facultad_3.py          # Aplicación FastAPI
├── nginx.conf                   # Configuración del proxy inverso
├── requirements.txt             # Dependencias Python
└── README.md                    # Documentación general
```

---

## 📄 Descripción de Archivos CSS

### `css/styles.css`

**Propósito:** Estilos globales y componentes reutilizables

**Contenido:**

- 🎨 Sistema de variables de marca (`--color-*`)
- 🌓 Definiciones de temas (dark/light mode)
- 🔤 Estilos de tipografía
- 📐 Estilos de componentes globales (header, tabla, alertas)
- 📱 Clases utilitarias

**Uso en todos los HTML**

### `css/forms.css`

**Propósito:** Estilos específicos de formularios

**Contenido:**

- 📝 Estilos de inputs, selects, textareas
- 🔘 Estilos de botones y checkboxes
- 📋 Grillas responsivas para formularios
- ✅ Validación visual
- ⚠️ Mensajes de error y ayuda
- ⏳ Animaciones de carga

**Uso en:** `formulario_crear_alumnos.html`, `formulario_alumnos.html`

---

## 📜 Descripción de Archivos JavaScript

### `js/theme.js`

**Propósito:** Gestionar el sistema de tema claro/oscuro

**Funcionalidad:**

- Detectar tema guardado en localStorage
- Aplicar tema al DOM (`data-theme` attribute)
- Actualizar botones de toggle
- Persistir preferencias del usuario
- **Tamaño:** ~3 KB | **Dependencias:** ninguna

**Exporta:** Clase `ThemeManager`

**Uso:** Automático en todos los HTML

---

### `js/form-handler.js`

**Propósito:** Manejador genérico de formularios con validación y feedback

**Funcionalidad:**

- Capturar envío de formularios
- Recolectar datos del formulario
- Enviar a API mediante AJAX (POST)
- Mostrar mensajes de éxito/error
- Limpiar formulario tras éxito
- Manejar estados de botones (carga)
- Opción de redirección tras éxito
- **Tamaño:** ~4 KB | **Dependencias:** ninguna

**Exporta:** Clase `FormHandler`

**Uso:**

```javascript
new FormHandler('formularioId', '/ruta/api/', {
  redirectOnSuccess: false,
  showSuccessTime: 3000,
});
```

**Utilizado en:** `formulario_crear_alumnos.html`

---

### `js/utils.js`

**Propósito:** Funciones utilitarias reutilizables en todo el proyecto

**Funciones disponibles:**

| Función                                | Descripción                           |
| -------------------------------------- | ------------------------------------- |
| `objectToFormData(obj)`                | Convierte objeto a FormData           |
| `fetchWithErrorHandling(url, options)` | Fetch con manejo de errores           |
| `formatDate(dateString)`               | Formatea fecha a formato legible (ES) |
| `validateNIF(nif)`                     | Valida NIF español                    |
| `validateEmail(email)`                 | Valida formato de email               |
| `showConfirmDialog(title, msg)`        | Modal de confirmación                 |
| `debounce(func, wait)`                 | Debounce function                     |
| `throttle(func, limit)`                | Throttle function                     |
| `saveToLocalStorage(key, data)`        | Guarda datos en localStorage          |
| `getFromLocalStorage(key, default)`    | Recupera datos de localStorage        |
| `clearLocalStorage(key)`               | Limpia localStorage                   |

**Tamaño:** ~3 KB | **Dependencias:** ninguna

---

## 🔗 Estructura de Importación en HTML

Todos los HTML ahora siguen este patrón:

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <!-- Meta y Tailwind -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/..." rel="stylesheet" />

    <!-- Estilos Globales (en TODOS) -->
    <link rel="stylesheet" href="/css/styles.css" />

    <!-- Estilos específicos (si aplica) -->
    <link rel="stylesheet" href="/css/forms.css" />
  </head>
  <body>
    <!-- Contenido HTML -->

    <!-- Scripts -->
    <script src="/js/utils.js"></script>
    <!-- Siempre primero -->
    <script src="/js/theme.js"></script>
    <!-- Siempre segundo -->
    <script src="/js/form-handler.js"></script>
    <!-- Si es necesario -->

    <!-- Scripts Inline (solo lógica estrictamente necesaria) -->
    <script>
      // Inicializar componentes específicos de la página
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
          new FormHandler('formId', '/api/endpoint/');
        });
      }
    </script>
  </body>
</html>
```

---

## 📱 Por Página - Qué Se Carga

| Página                          | CSS                   | JS                                  | Propósito           |
| ------------------------------- | --------------------- | ----------------------------------- | ------------------- |
| `alumnos.html`                  | styles.css            | theme.js                            | Listar alumnos      |
| `home.html`                     | styles.css            | theme.js                            | Detalle de alumno   |
| `resultado_alumnos.html`        | styles.css            | theme.js                            | Resultados búsqueda |
| `formulario_alumnos.html`       | styles.css, forms.css | theme.js                            | Formulario búsqueda |
| `formulario_crear_alumnos.html` | styles.css, forms.css | theme.js, form-handler.js, utils.js | Formulario creación |

---

## 🎨 Variables de Marca Disponibles

Definidas en `css/styles.css`:

```css
--color-negro-carbon: #0e0e11 /* Fondo oscuro */ --color-gris-antracita: #1c1e22
  /* Fondo secundario */ --color-gris-acero: #3a3d42 /* Fondo terciario */
  --color-gris-tecnico: #b5b8be /* Texto secundario */
  --color-verde-criptico: #3aff7a /* Acento principal */
  --color-blanco-tecnico: #f2f3f5 /* Texto principal */;
```

Se invierten automáticamente con `[data-theme='light']`

---

## ⚙️ Ventajas de Esta Estructura

✅ **Separación de Concerns:** CSS y JS separados del HTML  
✅ **Reutilización:** Componentes CSS y funciones JS se usan en múltiples páginas  
✅ **Mantenibilidad:** Cambios centralizados en un solo archivo  
✅ **Caché de Navegador:** Archivos se cachean automáticamente  
✅ **Rendimiento:** Menor tamaño de HTML, menos redundancia  
✅ **Escalabilidad:** Fácil agregar nuevas páginas  
✅ **Debugging:** Código organizado y fácil de localizar errores

---

## 📝 Notas Importantes

1. **Rutas:** Las rutas `/css/` y `/js/` deben estar disponibles en Nginx o FastAPI
2. **Media Types:** Nginx debe servir con los tipos MIME correctos:
   - `text/css` para `.css`
   - `application/javascript` para `.js`
3. **Tailwind:** Se sigue usando Tailwind CDN para clases de utilidad
4. **Jinja2:** Los templates HTML pueden contener lógica de Jinja2 (loops, condicionales, etc.)

---

## 🚀 Próximas Mejoras

- [ ] Minificar CSS y JS para producción
- [ ] Crear archivo de configuración global (config.js)
- [ ] Agregar servicios (API client)
- [ ] Crear componentes Web reutilizables
- [ ] Configurar bundler (Webpack/Vite) si es necesario

---

**Última actualización:** 2026-06-15  
**Mantenedor:** Equipo de Desarrollo
