document.addEventListener('DOMContentLoaded', function () {
  const drawer = document.getElementById('drawer');
  const drawerClose = document.getElementById('drawer-close');
  const drawerBackdrop = document.getElementById('drawer-backdrop');
  const drawerTriggers = document.querySelectorAll('.drawer-trigger');

  if (drawer && drawerClose && drawerBackdrop) {
    drawerTriggers.forEach(function (trigger) {
      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        drawer.classList.add('show');
        drawerBackdrop.classList.add('show');
      });
    });

    drawerClose.addEventListener('click', function () {
      drawer.classList.remove('show');
      drawerBackdrop.classList.remove('show');
    });

    drawerBackdrop.addEventListener('click', function () {
      drawer.classList.remove('show');
      drawerBackdrop.classList.remove('show');
    });
  }
});
