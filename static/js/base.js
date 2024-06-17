document.addEventListener('DOMContentLoaded', function() {
    // When the DOM content is fully loaded, execute the following code

    // Select all elements with class 'dropdown-toggle'
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    // Add click event listener to each dropdown toggle
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(event) {
            // Prevent default link behavior (e.g., following href)
            event.preventDefault();

            // Get the parent element (dropdown menu)
            const parentDropdown = this.parentElement;

            // Check if the dropdown menu is currently open
            const isOpen = parentDropdown.classList.contains('open');

            // Close all dropdowns before opening the clicked one
            closeAllDropdowns();

            // If the dropdown menu is not open, open it
            if (!isOpen) {
                parentDropdown.classList.add('open');
            }
        });
    });

    // Close dropdowns when clicking outside any dropdown area
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.dropdown')) {
            closeAllDropdowns();
        }
    });

    // Function to close all dropdown menus
    function closeAllDropdowns() {
        const openDropdowns = document.querySelectorAll('.dropdown.open');
        openDropdowns.forEach(dropdown => {
            dropdown.classList.remove('open');
        });
    }
});
