document.addEventListener('DOMContentLoaded', function () {
  // ── Desktop user menu dropdown ──────────────────────────
  const userBtn = document.getElementById('userMenuBtn');
  const userDD  = document.getElementById('userDropdown');
  if (userBtn && userDD) {
    userBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      userDD.classList.toggle('open');
    });
    document.addEventListener('click', function () {
      userDD.classList.remove('open');
    });
  }

  // ── Mobile hamburger menu ───────────────────────────────
  // Removed: Bootstrap offcanvas handles this now

  // ── Admin sidebar toggle (mobile) ───────────────────────
  const sidebarToggle = document.getElementById('adminSidebarToggle');
  const adminSidebar  = document.getElementById('adminSidebar');
  if (sidebarToggle && adminSidebar) {
    sidebarToggle.addEventListener('click', function () {
      const isOpen = adminSidebar.classList.toggle('open');
      sidebarToggle.querySelector('.toggle-label').textContent = isOpen ? 'Hide Menu' : 'Admin Menu';
    });
  }

  // ── Admin dashboard tab switching ───────────────────────
  const tabLinks = document.querySelectorAll('[data-tab]');
  const tabPanes = document.querySelectorAll('[data-pane]');
  if (tabLinks.length) {
    tabLinks.forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const target = this.dataset.tab;
        tabLinks.forEach(l => l.classList.remove('active'));
        tabPanes.forEach(p => p.style.display = 'none');
        this.classList.add('active');
        const pane = document.querySelector('[data-pane="' + target + '"]');
        if (pane) pane.style.display = '';
      });
    });
    // Show first pane by default
    const firstPane = document.querySelector('[data-pane]');
    if (firstPane) {
      tabPanes.forEach(p => { if (p !== firstPane) p.style.display = 'none'; });
    }
  }

  // ── Animate bar chart fills ─────────────────────────────
  document.querySelectorAll('.bar-fill[data-width]').forEach(function (bar) {
    setTimeout(function () {
      bar.style.width = bar.dataset.width + '%';
    }, 300);
  });
});
