document.addEventListener("DOMContentLoaded", function () {
    var reveals = document.querySelectorAll(".reveal");
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("in-view");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });
    reveals.forEach(function (el) { observer.observe(el); });

    var cta = document.getElementById("ctaScroll");
    if (cta) {
        cta.addEventListener("click", function () {
            cta.classList.add("glitch");
            setTimeout(function () {
                cta.classList.remove("glitch");
                var target = document.getElementById("grid-section");
                if (target) target.scrollIntoView({ behavior: "smooth" });
            }, 350);
        });
    }
});
