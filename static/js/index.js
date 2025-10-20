function initializeProjectInteraction() {

    const currentLang = localStorage.getItem('preferredLang') || 'english';
    const JSONfilePath = `static/json/lang/${currentLang}.json`;
    const projectItems = document.querySelectorAll(".back-content p");

    const dynamicContainer = document.getElementById("dynamic-project-container");
    const detailElements = {
        explanation: document.getElementById("dynamic-text-explanation"),
        utility: document.getElementById("dynamic-text-utility"),
        howTo: document.getElementById("dynamic-text-howto"),
        output: document.getElementById("dynamic-text-output")
    };

    function resetSelection() {
        projectItems.forEach(item => {
            item.classList.remove("selected", "not-selected");
        });
    }

    function updateProjectDetails(projectId, projectData) {
        const getTextContent = (detailType) => {
            const content = projectData?.[detailType]?.[projectId];
            return content || "Details not available.";
        };

        Object.keys(detailElements).forEach(key => {
            const content = getTextContent(key);
            detailElements[key].textContent = content;
        });

        const titleElement = document.getElementById('dynamic-text-title');
        if (titleElement) {
            titleElement.textContent = projectData?.title?.[projectId] || projectId;
        }
    }

    fetch(JSONfilePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const projectData = data["projects-description"];
            projectItems.forEach((item, index) => {

                item.addEventListener("click", (event) => {
                    event.preventDefault();
                    event.stopPropagation();

                    const alreadySelected = item.classList.contains("selected");
                    if (alreadySelected) {
                        resetSelection();
                        dynamicContainer.style.display = "none";
                        return;
                    }
                    resetSelection();

                    item.classList.add("selected");
                    projectItems.forEach(p => {
                        if (p !== item) {
                            p.classList.add("not-selected");
                        }
                    });

                    const projectId = item.getAttribute("data-id");
                    updateProjectDetails(projectId, projectData);
                    dynamicContainer.style.display = "block";
                    setTimeout(() => {
                        dynamicContainer.scrollIntoView({
                            behavior: "smooth",
                            block: "start"
                        });
                    }, 100);
                });
            });
            document.addEventListener('click', (event) => {
                const clickedOnProject = event.target.closest(".back-content p");
                const clickedOnContainer = event.target.closest("#dynamic-project-container");

                if (!clickedOnProject && !clickedOnContainer) {
                    resetSelection();
                    dynamicContainer.style.display = "none";
                }
            });
        })
        .catch(error => {
            console.error(error);
            console.error(error.message);
        });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeProjectInteraction);
} else {
    initializeProjectInteraction();
}

function initializeProjectFilter() {
    const searchInput = document.getElementById('project-search');
    const filterTags = document.querySelectorAll('.filter-tag');
    const projectCards = document.querySelectorAll('.project-card');
    const modal = document.querySelector('.project-modal');
    const modalOverlay = document.querySelector('.modal-overlay');
    const modalClose = document.querySelector('.modal-close');

    let activeFilter = 'all';
    let searchTerm = '';

    function filterProjects() {
        projectCards.forEach(card => {
            const tags = card.dataset.tags.split(',');
            const title = card.querySelector('.project-title').textContent.toLowerCase();
            const description = card.querySelector('.project-description').textContent.toLowerCase();

            const matchesFilter = activeFilter === 'all' || tags.includes(activeFilter);
            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);

            card.style.display = matchesFilter && matchesSearch ? 'block' : 'none';
        });
    }

    searchInput.addEventListener('input', (e) => {
        searchTerm = e.target.value.toLowerCase();
        filterProjects();
    });

    filterTags.forEach(tag => {
        tag.addEventListener('click', () => {
            filterTags.forEach(t => t.classList.remove('active'));
            tag.classList.add('active');
            activeFilter = tag.dataset.filter;
            filterProjects();
        });
    });

    projectCards.forEach(card => {
        card.addEventListener('click', () => {
            const projectId = card.dataset.id;
            modal.dataset.currentProjectId = projectId;
            // const projectData = window.projectTranslations;
            updateModalContent(projectId);
            modal.style.display = 'block';
            modalOverlay.style.display = 'block';
        });
    });

    modalClose.addEventListener('click', () => {
        modal.style.display = 'none';
        modalOverlay.style.display = 'none';
    });

    modalOverlay.addEventListener('click', () => {
        modal.style.display = 'none';
        modalOverlay.style.display = 'none';
    });
}

function updateModalContent(projectId) {
    const projectData = window.projectTranslations;
    if (!projectData) {
        console.error('No project translations found');
        return;
    }

    const modalElements = {
        title: document.querySelector('.modal-title'),
        explanation: document.getElementById('dynamic-text-explanation'),
        utility: document.getElementById('dynamic-text-utility'),
        howTo: document.getElementById('dynamic-text-howto'),
        output: document.getElementById('dynamic-text-output')
    };

    const sections = {
        title: projectId,
        explanation: projectData.explanation?.[projectId],
        utility: projectData.utility?.[projectId],
        howTo: projectData.howTo?.[projectId],
        output: projectData.output?.[projectId]
    };

    Object.entries(modalElements).forEach(([key, element]) => {
        if (element) {
            let content = sections[key] || `${key} not available.`;
            if (key === 'title') {
                content = content
                    .split('-')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');
            }

            element.textContent = content;
        }
    });
}

document.addEventListener('DOMContentLoaded', initializeProjectFilter);