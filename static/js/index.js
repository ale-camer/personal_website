//Home Page Functionalities

const JSONfilePath = 'static/json/config.json';
const projectItems = document.querySelectorAll(".back-content p");
const dynamicContainer = document.getElementById("dynamic-project-container");
const detailElements = {
    explanation: document.getElementById("dynamic-text-explanation"),
    utility: document.getElementById("dynamic-text-utility"),
    howTo: document.getElementById("dynamic-text-howto"),
    output: document.getElementById("dynamic-text-output")
};

function resetSelection() {
    projectItems.forEach(item => item.classList.remove("selected", "not-selected"));
}

function updateProjectDetails(projectId, projectData) {
    const getTextContent = (detailType) => projectData?.[detailType]?.[projectId] || "Details not available.";
    
    Object.keys(detailElements).forEach(key => {
        detailElements[key].textContent = getTextContent(key);
    });
}

fetch(JSONfilePath)
    .then(response => response.json())
    .then(data => {
        const projectData = data["projects-description"];

        projectItems.forEach(item => {
            item.addEventListener("click", () => {
                const alreadySelected = item.classList.contains("selected");

                if (alreadySelected) {
                    resetSelection();
                    dynamicContainer.style.display = "none";
                    return;
                }

                resetSelection();
                item.classList.add("selected");
                projectItems.forEach(p => {
                    if (p !== item) p.classList.add("not-selected");
                });

                const projectId = item.getAttribute("data-id");
                updateProjectDetails(projectId, projectData);

                dynamicContainer.style.display = "block";
                dynamicContainer.scrollIntoView({ behavior: "smooth", block: "start" });
            });
        });
    })
    .catch(error => console.error('Error al cargar los datos:', error));

document.addEventListener('click', (event) => {
    if (!event.target.closest(".back-content p") && !event.target.closest("#dynamic-project-container")) {
        resetSelection();
        dynamicContainer.style.display = "none";
    }
});