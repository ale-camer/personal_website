const projectDetailsExplanation = {
    "keyphrase-extraction": "Helps identify and extract important terms and phrases from texts summarizing the main content.",
    "seasonality-prediction": "Forecast values of time series based on its seasonal patterns.",
    "whatsapp": "Generate a dashboard with key visualizations in order to analyze both individual and group chats.",
    "world-bank": "Deploy data collected by the World Bank.",
    "algorithmic-trading": "Backtesting of buy-and-hold strategy of Fortune 500 companies by selecting them with clusterization.",
    "trends-data-science": "Analysis of Data Science job postings from timesjobs.com and flexjobs.com in 2022.",
    "macro-employment": "Visualize World Bankasdadal economic trends and insights.",
    "linear-algebra": "Theorical explanation of linear algebra concepts use in data science.",
    "vector-norms": "Practical uses of a linear algebra tools in regular data science tasks.",
};

const projectDetailsUtility = {
    "keyphrase-extraction": "Analyzing documents, optimizing search engine results or summarizing content.",
    "seasonality-prediction": "Any time serie with seasonal pattern.",
    "whatsapp": "Find communication patters and sentiments.",
    "world-bank": "Visualize World Bank data to explore global economic trends and insights.",
    "algorithmic-trading": "Select stocks automatically for a stock fund that rebalanced regularly.",
    "trends-data-science": "Visualize the priorities of the market.",
    "macro-employment": "Understand the consequences of economic policies in the GDP and therefore in the labour market.",
    "linear-algebra": "Learn the basics in the topic.",
    "vector-norms": "Learn how some math impact in data science tasks.",
};

const projectDetailsHowTo = {
    "keyphrase-extraction": "Upload a text file, specify the number of N-grams (sequence of n elements) and results (rows) per N-gram and hit the Extract Keyphrases' button.",
    "seasonality-prediction": "Upload an Excel file with just one column of numeric data and a header, select the periodicty (e.g., 4 for quarterly data) and hit the 'Calculate Prediction' button",
    "whatsapp": "Export WhatsApp chat by clicking on the three dots in the upper-right corner of the phone screen in the conversation, select 'More' and then 'Export Chat'. After that upload the text file, select the language in which the conversation was held and hit the 'Analyze Chat' button.",
    "world-bank": "Select: indicator (e.g. GDP per Capita), data type and the year or country depending on the data type choosen and hit the 'Show Results' button. After this, if you want the raw data hit the 'Download CSV' button and/or if you want an interactive graph hit the 'Interactive Graph' button.",
    "algorithmic-trading": "Open and read it.",
    "trends-data-science": "Open and read it.",
    "macro-employment": "Open and read it. There's the Spanish and the English version.",
    "linear-algebra": "Open and read it.",
    "vector-norms": "Open and read it.",
};

const projectDetailsOutput = {
    "keyphrase-extraction": "Tables with most repeated N-grams.",
    "seasonality-prediction": "Table with forecast for next cycle and graphs of: original time serie, comparing prediction of last cycle and real last cycle and time serie along with next cycle forecast.",
    "whatsapp": "Interactive dashboard.",
    "world-bank": "Table with data requested, option to download the table in a CSV format and an interactive grapth.",
    "algorithmic-trading": "None.",
    "trends-data-science": "None.",
    "macro-employment": "None.",
    "linear-algebra": "None.",
    "vector-norms": "None.",
};

const projectItems = document.querySelectorAll(".back-content p");
const dynamicContainer = document.getElementById("dynamic-project-container");

function resetSelection() {
    projectItems.forEach(p => p.classList.remove("selected", "not-selected"));
}

function updateProjectDetails(projectId) {
    document.getElementById("dynamic-text-explanation").textContent = projectDetailsExplanation[projectId] || "Details not available.";
    document.getElementById("dynamic-text-utility").textContent = projectDetailsUtility[projectId] || "Details not available.";
    document.getElementById("dynamic-text-howto").textContent = projectDetailsHowTo[projectId] || "Details not available.";
    document.getElementById("dynamic-text-output").textContent = projectDetailsOutput[projectId] || "Details not available.";
}

projectItems.forEach(item => {
    item.addEventListener("click", function () {

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
        updateProjectDetails(projectId);

        dynamicContainer.style.display = "block";
        dynamicContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    });
});

document.addEventListener('click', function (event) {
    const clickedInsideItem = event.target.closest(".back-content p");
    const clickedInsideContainer = event.target.closest("#dynamic-project-container");

    if (!clickedInsideItem && !clickedInsideContainer) {
        resetSelection();
        dynamicContainer.style.display = "none";
    }
});
