// Home Page Functionalities - Versión Corregida

const JSONfilePath = 'static/json/config.json';

function initializeProjectInteraction() {
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