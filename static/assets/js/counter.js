document.addEventListener("DOMContentLoaded", function () {
    function animateNumber(element, start, end, duration) {
        let startTime = null;
        function step(currentTime) {
            if (!startTime) startTime = currentTime;
            let elapsed = currentTime - startTime;
            let progress = Math.min(elapsed / duration, 1);

            let easingProgress = progress < 0.8 ? (progress * 2) : (1 - Math.pow(1 - progress, 4));
            let currentValue = Math.round(easingProgress * (end - start) + start);

            if (currentValue > end) {
                currentValue = end;
            }

            element.textContent = currentValue;
            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                element.textContent = end;
            }
        }
        requestAnimationFrame(step);
    }

    function handleIntersection(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                let target = entry.target;
                let endValue = parseInt(target.dataset.value, 10);
                animateNumber(target, 0, endValue, 2000);
                observer.unobserve(target);
            }
        });
    }

    let observer = new IntersectionObserver(handleIntersection, {
        root: null,
        rootMargin: "0px",
        threshold: 0.5
    });

    document.querySelectorAll(".counter").forEach(counter => {
        observer.observe(counter);
    });
});