// base.js
document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector(".navbar");
    const blueSections = document.querySelectorAll(".two, .three, .four, .five");
    const navbarButtons = document.querySelector(".navbar-buttons");

    window.addEventListener("scroll", () => {
        const scrollPosition = window.scrollY;

        if (scrollPosition > 0) {
            // If scrolled down, add a CSS class to change the navbar color
            navbar.classList.add("scrolled");
            // Also add the class to change button colors
            navbarButtons.classList.add("scrolled-buttons");
        } else {
            // If at the top, remove the class to reset the navbar color
            navbar.classList.remove("scrolled");
            // Also remove the class to reset button colors
            navbarButtons.classList.remove("scrolled-buttons");
        }

        // Check if the user is in a blue section and adjust navbar text color accordingly
        blueSections.forEach((section) => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 0 && rect.bottom >= 0) {
                // Section is currently in view
                navbar.classList.add("blue-section");
                // Also add the class to change button colors
                navbarButtons.classList.add("blue-buttons");
            } else {
                navbar.classList.remove("blue-section");
                // Also remove the class to reset button colors
                navbarButtons.classList.remove("blue-buttons");
            }
        });
    });
});


