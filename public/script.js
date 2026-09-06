// Cambiar estilo de la barra de navegación al hacer scroll
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
  // Verificamos que el navbar exista en el DOM antes de manipularlo
  if (navbar) {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
});

// Manejo sencillo del formulario de suscripción
const ctaForm = document.getElementById('ctaForm');

if (ctaForm) {
  ctaForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = ctaForm.querySelector('input');
    
    if (input && input.value.trim() !== '') {
      alert(`¡Gracias por registrarte! Hemos recibido el correo: ${input.value}`);
      input.value = '';
    }
  });
}