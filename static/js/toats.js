document.querySelectorAll('.toast').forEach(function (toast) {
    // Появление
    toast.classList.add("translate-x-full", "opacity-0");

    setTimeout(() => {
        toast.classList.remove("translate-x-full", "opacity-0");
        toast.classList.add("translate-x-0", "opacity-100");
    }, 0);

    // Скрытие через 5 секунд
    setTimeout(() => {
        toast.classList.add("opacity-0", "translate-x-full");
    }, 5000);

    // Полное скрытие
    setTimeout(() => {
        toast.classList.add("hidden");
    }, 5200);
});