/**
 * Utility Functions
 * Funciones utilitarias generales
 */

/**
 * Convierte un objeto en formato FormData de JSON
 */
function objectToFormData(obj) {
  const formData = new FormData();
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      formData.append(key, obj[key]);
    }
  }
  return formData;
}

/**
 * Realiza una petición fetch con manejo de errores
 */
async function fetchWithErrorHandling(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

/**
 * Formatea una fecha en formato legible
 */
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('es-ES', options);
}

/**
 * Valida un NIF español
 */
function validateNIF(nif) {
  const nifRegex = /^[0-9]{8}[A-Z]$/i;
  if (!nifRegex.test(nif)) {
    return false;
  }

  const letters = 'TRWAGMYFPDXBNJZSQVHLCKE';
  const number = parseInt(nif.substring(0, 8), 10);
  const letter = nif.charAt(8).toUpperCase();
  return letters[number % 23] === letter;
}

/**
 * Valida un email
 */
function validateEmail(email) {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
}

/**
 * Muestra un modal de confirmación
 */
function showConfirmDialog(title, message) {
  return new Promise((resolve) => {
    if (confirm(`${title}\n\n${message}`)) {
      resolve(true);
    } else {
      resolve(false);
    }
  });
}

/**
 * Debounce function para limitar llamadas a funciones
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function para limitar frecuencia de llamadas
 */
function throttle(func, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Guarda datos en localStorage de forma segura
 */
function saveToLocalStorage(key, data) {
  try {
    localStorage.setItem(key, JSON.stringify(data));
    return true;
  } catch (error) {
    console.error('Error saving to localStorage:', error);
    return false;
  }
}

/**
 * Recupera datos de localStorage de forma segura
 */
function getFromLocalStorage(key, defaultValue = null) {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error('Error reading from localStorage:', error);
    return defaultValue;
  }
}

/**
 * Limpia localStorage
 */
function clearLocalStorage(key = null) {
  try {
    if (key) {
      localStorage.removeItem(key);
    } else {
      localStorage.clear();
    }
    return true;
  } catch (error) {
    console.error('Error clearing localStorage:', error);
    return false;
  }
}
