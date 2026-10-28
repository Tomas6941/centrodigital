// Centro de Estudiantes Digital — interacciones
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('navToggle');
  var menu = document.getElementById('navMenu');
  var more = document.querySelector('.nav-more');
  var moreBtn = more && more.querySelector('button');

  function closeMenu() {
    if (menu) menu.classList.remove('active');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
  }
  function closeMore() {
    if (more) { more.classList.remove('open'); moreBtn.setAttribute('aria-expanded', 'false'); }
  }

  if (toggle && menu) {
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = menu.classList.toggle('active');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
  }
  if (moreBtn) {
    moreBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = more.classList.toggle('open');
      moreBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  document.addEventListener('click', function (e) {
    if (more && !more.contains(e.target)) closeMore();
    if (menu && toggle && !menu.contains(e.target) && !toggle.contains(e.target)) closeMenu();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeMore(); closeMenu(); }
  });

  // Mensajes flash: se ocultan solos a los 6 s
  document.querySelectorAll('.flash').forEach(function (flash) {
    setTimeout(function () { flash.remove(); }, 6000);
  });
});
