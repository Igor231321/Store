document.addEventListener('DOMContentLoaded', function() {
  const dropdownButton = document.getElementById('dropdownButton');
  const dropdownMenu = document.getElementById('dropdownMenu');

  dropdownButton.addEventListener('click', function(event) {
    // Добавляем класс bg-darkgold при нажатии
    dropdownButton.classList.add('active');

    // Переключаем видимость меню с анимацией
    if (dropdownMenu.classList.contains('hidden')) {
      dropdownMenu.classList.remove('hidden');
      setTimeout(function() {
        dropdownMenu.classList.remove('opacity-0', 'scale-95');
        dropdownMenu.classList.add('opacity-100', 'scale-100');
      }, 10); // Немедленно применяем классы для анимации
    } else {
      // Плавно исчезаем
      dropdownMenu.classList.remove('opacity-100', 'scale-100');
      dropdownMenu.classList.add('opacity-0', 'scale-95');
      
      // После анимации скрываем меню
      setTimeout(function() {
        dropdownMenu.classList.add('hidden');
      }, 300); // Ожидаем завершения анимации
    }

    // Предотвращаем распространение события, чтобы не сработал закрытие меню
    event.stopPropagation();
  });

  // Закрытие меню при клике вне его
  document.addEventListener('click', function(event) {
    if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
      dropdownMenu.classList.remove('opacity-100', 'scale-100');
      dropdownMenu.classList.add('opacity-0', 'scale-95');
      
      setTimeout(function() {
        dropdownMenu.classList.add('hidden');
      }, 300); // Ожидаем завершения анимации

      // Убираем класс bg-darkgold с кнопки
      dropdownButton.classList.remove('active');
    }
  });
});
