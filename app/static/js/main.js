// Centro de Estudiantes Digital - Apple Style Interactions

document.addEventListener('DOMContentLoaded', function() {
  // Mobile Navigation Toggle
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function(e) {
      e.stopPropagation();
      navMenu.classList.toggle('active');
      
      // Update toggle icon
      if (navMenu.classList.contains('active')) {
        navToggle.textContent = '✕';
      } else {
        navToggle.textContent = '☰';
      }
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('active');
        navToggle.textContent = '☰';
      }
    });
    
    // Close menu when clicking on a link
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        navMenu.classList.remove('active');
        navToggle.textContent = '☰';
      });
    });
  }
  
  // Add subtle press feedback to buttons and cards
  const interactiveElements = document.querySelectorAll('.btn, .dashboard-card, .nav-link');
  
  interactiveElements.forEach(el => {
    el.addEventListener('pointerdown', function() {
      // Add a subtle class for press state if needed
      this.style.transition = 'all 100ms cubic-bezier(0.25, 0.1, 0.25, 1)';
    });
  });
  
  // Auto-hide flash messages after 5 seconds
  const flashMessages = document.querySelectorAll('.flash');
  flashMessages.forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'all 200ms cubic-bezier(0.25, 0.1, 0.25, 1)';
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-8px)';
      setTimeout(() => {
        flash.remove();
      }, 200);
    }, 5000);
  });
});
