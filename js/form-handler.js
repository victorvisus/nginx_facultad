/**
 * Form Handler
 * Maneja el envío de formularios con validación y feedback del usuario
 */

class FormHandler {
  constructor(formId, submitUrl, options = {}) {
    this.form = document.getElementById(formId);
    this.submitUrl = submitUrl;
    this.options = {
      redirectOnSuccess: false,
      redirectUrl: '/',
      showSuccessTime: 3000,
      ...options,
    };

    if (this.form) {
      this.init();
    }
  }

  init() {
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  async handleSubmit(e) {
    e.preventDefault();

    const data = this.getFormData();

    try {
      this.setButtonState(true);
      const response = await this.submitForm(data);

      if (response.ok) {
        const result = await response.json();
        this.showSuccess(result);

        // Limpiar formulario
        this.form.reset();

        // Redirigir si es necesario
        if (this.options.redirectOnSuccess) {
          setTimeout(() => {
            window.location.href = this.options.redirectUrl;
          }, this.options.showSuccessTime);
        } else {
          // Ocultar alerta después del tiempo especificado
          setTimeout(() => {
            this.hideAlert();
          }, this.options.showSuccessTime);
        }
      } else {
        const error = await response.json();
        this.showError(error.detail || 'Error desconocido');
      }
    } catch (err) {
      this.showError(`Error de conexión: ${err.message}`);
    } finally {
      this.setButtonState(false);
    }
  }

  getFormData() {
    const formData = new FormData(this.form);
    const data = {};

    for (let [key, value] of formData.entries()) {
      // Convertir booleanos si es necesario
      if (value === 'true') {
        data[key] = true;
      } else if (value === 'false') {
        data[key] = false;
      } else if (key === 'beca' && value) {
        data[key] = value === 'true';
      } else {
        data[key] = value || null;
      }
    }

    return data;
  }

  async submitForm(data) {
    return fetch(this.submitUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  }

  showSuccess(result) {
    this.showAlert(
      `✅ ¡Operación exitosa! ${result.id ? `(ID: ${result.id})` : ''}`,
      'success',
    );
  }

  showError(message) {
    this.showAlert(`❌ Error: ${message}`, 'error');
  }

  showAlert(message, type = 'info') {
    let alertContainer = document.getElementById('alertContainer');
    let alertMessage = document.getElementById('alertMessage');

    if (!alertContainer) {
      // Crear contenedor si no existe
      alertContainer = document.createElement('div');
      alertContainer.id = 'alertContainer';
      alertContainer.className = 'alert-box';
      alertMessage = document.createElement('p');
      alertMessage.id = 'alertMessage';
      alertContainer.appendChild(alertMessage);
      this.form.parentNode.insertBefore(alertContainer, this.form);
    }

    alertMessage.textContent = message;
    alertContainer.className = `alert-box alert-${type}`;
    alertContainer.classList.remove('hidden');
  }

  hideAlert() {
    const alertContainer = document.getElementById('alertContainer');
    if (alertContainer) {
      alertContainer.classList.add('hidden');
    }
  }

  setButtonState(isLoading) {
    const submitBtn = this.form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = isLoading;
      submitBtn.innerHTML = isLoading
        ? '<span class="loading"></span> Enviando...'
        : 'Registrar Alumno';
    }
  }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    // Este será inicializado en cada página según sea necesario
  });
}
