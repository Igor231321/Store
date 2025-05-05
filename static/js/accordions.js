var acc = document.getElementsByClassName("accordion");

for (var i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        var content = panel.querySelector('.panel-content');

        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
            panel.classList.remove('show');
        } else {
            panel.style.maxHeight = content.scrollHeight + 32 + "px"; // 32px padding
            panel.classList.add('show');
        }
    })}