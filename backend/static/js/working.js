document.addEventListener("DOMContentLoaded", function() {
    const items = document.querySelectorAll(".timeline-item");

    function revealOnScroll() {
        const triggerBottom = window.innerHeight * 0.85;

        items.forEach(item => {
            const itemTop = item.getBoundingClientRect().top;
            if (itemTop < triggerBottom) {
                item.classList.add("show");
            }
        });
    }

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll();
});
