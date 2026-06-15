/**
 * Theme Manager
 * Maneja el sistema de tema claro/oscuro con persistencia en localStorage
 */

class ThemeManager {
  constructor(storageKey = 'theme') {
    this.storageKey = storageKey;
    this.defaultTheme = 'dark';
    this.init();
  }

  init() {
    const savedTheme = this.getSavedTheme();
    this.setTheme(savedTheme);
    this.attachEventListeners();
  }

  getSavedTheme() {
    return localStorage.getItem(this.storageKey) || this.defaultTheme;
  }

  getCurrentTheme() {
    return (
      document.documentElement.getAttribute('data-theme') || this.defaultTheme
    );
  }

  setTheme(theme) {
    if (!['light', 'dark'].includes(theme)) {
      theme = this.defaultTheme;
    }
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(this.storageKey, theme);
    this.updateThemeButtons();
  }

  toggleTheme() {
    const currentTheme = this.getCurrentTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    this.setTheme(newTheme);
  }

  updateThemeButtons() {
    const buttons = document.querySelectorAll('button#theme-toggle');
    const currentTheme = this.getCurrentTheme();

    buttons.forEach((btn) => {
      if (currentTheme === 'dark') {
        btn.textContent = '🌙 Claro';
        btn.classList.remove('bg-gray-700', 'text-white');
        btn.classList.add('bg-[#3AFF7A]', 'text-[#0E0E11]');
      } else {
        btn.textContent = '☀️ Oscuro';
        btn.classList.remove('bg-[#3AFF7A]', 'text-[#0E0E11]');
        btn.classList.add('bg-gray-700', 'text-white');
      }
    });
  }

  attachEventListeners() {
    document.addEventListener('click', (e) => {
      if (e.target && e.target.id === 'theme-toggle') {
        this.toggleTheme();
      }
    });
  }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
  });
} else {
  new ThemeManager();
}
