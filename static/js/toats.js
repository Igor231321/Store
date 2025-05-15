document.querySelectorAll(".toast").forEach((toast) => {
    setTimeout(() => {
      toast.classList.remove("animate-slide-in");
      toast.classList.add("animate-slide-out");
    }, 5000);

    setTimeout(() => {
      toast.remove();
    }, 5400);
  });