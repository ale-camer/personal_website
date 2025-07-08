//Project-wise Functionalities

document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(event) {
            event.preventDefault();
            const parentDropdown = this.parentElement;
            const isOpen = parentDropdown.classList.contains('open');
            closeAllDropdowns();
            if (!isOpen) {
                parentDropdown.classList.add('open');
            }
        });
    });

    document.addEventListener('click', function(event) {
        if (!event.target.closest('.dropdown')) {
            closeAllDropdowns();
        }
    });

    function closeAllDropdowns() {
        const openDropdowns = document.querySelectorAll('.dropdown.open');
        openDropdowns.forEach(dropdown => {
            dropdown.classList.remove('open');
        });
    }
    const cvAnchorLinks = document.querySelectorAll('#cv-menu a[href*="#"]');
    cvAnchorLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const linkUrl = new URL(link.href);
            const currentUrl = new URL(window.location.href);

            if (linkUrl.pathname === currentUrl.pathname) {
                event.preventDefault();
                const targetId = link.getAttribute('href').split('#')[1];
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
                closeAllDropdowns();
            }
        });
    });
});