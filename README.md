# Personal Website - Data Projects 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🌐 **Live Demo:** [Visit the project here](https://www.alejandrocamerlengo.com/)

A personal website showcasing data science projects, CV, and analytical articles. This portfolio is designed to demonstrate ideas and projects I have worked on, while also serving as a learning experience in web development. 👨‍💻

## 📋 Table of Contents

- [Live Demo](#live-demo)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Important Links](#important-links)
- [Footer](#footer)

## 🌐 Live Demo

Check out the live website [here](https://personal-website-gz63.onrender.com/).

## ✨ Key Features

- **Personal Portfolio:** Showcasing data projects and my CV.
- **Interactive Tools:**
  - Extract keyphrases from text.
  - Predict seasonal trends.
  - Analyze WhatsApp conversations.
  - Access and visualize World Bank API data.
- **Analytical Articles and Visual Insights:**
  - Data science job market trends.
  - Macroeconomics.
  - Mathematics.
  - Algorithmic trading.
- **Multi-language Support:** Uses JSON files to load text in different languages dynamically.

## 🛠️ Tech Stack

- **Frontend:**
  - HTML
  - SCSS
  - JavaScript
- **Backend & Data:**
  - Python (Flask, Dash)
  - Data manipulation and visualization: pandas, numpy, seaborn, matplotlib, plotly
  - Text processing: TextBlob, NLTK, unidecode, regex
  - Web and API tools: requests, tqdm, prettytable, folium, branca
  - Utility modules and structured programming: dataclasses, abc, os, re, zipfile, time
- **Other:**
  - Docker

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ale-camer/personal_website.git
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python main.py
   ```

## 💡 Usage

1.  **Run the application:** After completing the installation steps, execute `python main.py` to start the Flask server.
2.  **Access the Website:** Open your web browser and navigate to `http://127.0.0.1:5000/` or the address displayed in your console.
3.  **Explore Projects:** Use the navigation menu to explore different sections such as Keyphrase Extraction, Seasonality Prediction, WhatsApp Analysis, and World Bank Data.

### Keyphrase Extraction

1. Navigate to the "Keyphrase Extraction" page.
2. Upload a `.txt` file containing the text you want to analyze.
3. Adjust the number of n-grams and rows using the input controls.
4. Click the "Extract Keyphrases" button to process the text and display the results.
5. Download the results in TXT, Markdown, or PDF format.

### Seasonality Prediction

1.  Navigate to the "Seasonality Prediction" page.
2.  Upload an `.xlsx` or `.xls` file containing time series data.
3.  Specify the periodicity and number of lags.
4.  Click the "Predict Seasonality" button to generate forecasts and visualizations.
5.  Download the predictions and plots as a ZIP archive.

### WhatsApp Analysis

1. Navigate to the "WhatsApp Analysis" page.
2. Upload the exported WhatsApp chat `.txt` file.
3. Select the language of the chat.
4. Click the "Analyze Chat" button to view the interactive dashboard.

### World Bank Data

1. Navigate to the "World Bank Data" page.
2. Select an indicator and a type (country or year).
3. Choose an option and click the "Show Results" button to display the data in a table.
4. Download the data as a CSV file or view an interactive graph.

## 🗂️ Project Structure

```bash
personal_website/
├── app.py  # Web App project file (Flask instance and routes).
├── main.py  # Main project file (entry point to run the application).
├── modules/  # Contain Python modules.
│   ├── dash_app.py  # Dash App project file.
│   ├── keyphrase.py  # Contain functions for Keyphrases functionality.
│   ├── seasonality.py  # Refactored Seasonality Prediction functionality using two classes.
│   ├── utils.py  # Auxiliary functions.
│   ├── whatsapp.py  # Contain functions for WhatsApp functionality.
│   ├── world_bank.py  # Contain classes for World Bank functionality.
│   └── world_bank_utils.py  # World Bank Auxiliary functions.
├── README.md
├── requirements.txt
├── static/  # Contain static files (CSS, JS and images).
│   ├── css/  # Contain CSS main script.
│   │   ├── index.css  # Home Page Stylesheet File
│   │   ├── main.css  # Main Stylesheet File
│   │   ├── mi_cv.css  # My CV Stylesheet File
│   │   ├── seasonality.css  # Seasonality Prediction Stylesheet File
│   │   ├── utils.css  # Utils Project Stylesheet File
│   │   └── world_bank.css  # World Bank Stylesheet File
│   ├── images/  # Contain images for the UI.
│   │   ├── background.jpg
│   │   ├── email.png
│   │   ├── favicon.png
│   │   ├── gh.png
│   │   ├── li.png
│   │   └── profile.jpg
│   ├── js/  # Contain JavaScript scripts.
│   │   ├── base.js  # Project-wise Functionalities
│   │   ├── index.js  # Home Page Functionalities - Versión Corregida
│   │   ├── keyphrase.js  # Keyphrase Extraction Functionalities
│   │   ├── seasonality.js  # Seasonality Prediction Functionalities
│   │   ├── whatsapp.js  # WhatsApp Functionalities
│   │   └── world_bank.js  # World Bank Functionalities
│   ├── json/  # Contain JSON files.
│   │   ├── config.json
│   │   ├── readme.json
│   │   ├── stopwords.json
│   │   └── world_administrative_boundaries.json
│   ├── keyphrase/  # Contain Keyphrase Extraction functionality temporary files.
│   ├── seasonality/  # Contain Seasonality Prediction functionality temporary files.
│   └── world_bank/  # Contain World Bank functionality temporary files.
└── templates/  # Contain HTML templates.
    ├── base.html  # Base Project Template
    ├── index.html  # Home Page Template
    ├── Intro_to_Linear_Algebra_for_Data_Science.html  # Linear Algebra Functionality Template
    ├── keyphrase.html  # Keyphrase Extraction Functionality Template
    ├── macro_n_employment_english.html  # Macroeconomic (English) Functionality Template
    ├── macro_n_employment_spanish.html  # Macroeconomic (Spanish) Functionality Template
    ├── mi_cv.html  # My CV Template
    ├── seasonality.html  # Seasonality Prediction Functionality Template
    ├── Stock_Algorithmic_Trading_Strategy_Backtesting.html  # Algorithmic Trading Functionality Template
    ├── trends_in_data_science_labour_market.html  # Trends in Data Science Functionality Template
    ├── Vector_Norms_Applications_in_Data_Science.html  # Vector Nomrs Functionality Template
    ├── whatsapp.html  # WhatsApp Functionality Template
    └── world_bank.html  # World Bank Functionality Template
```

## ℹ️ API Reference

The project uses the World Bank API for fetching economic indicators. The core logic for interacting with the API is located in `modules/world_bank/core.py`. Here are some key API endpoints:

-   `https://api.worldbank.org/v2/country/all/indicator/{indicator_id}`: Downloads data for a specific indicator.
-   `https://api.worldbank.org/v2/country`: Retrieves a list of countries.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.

## 🛠️ Deployment

The application is containerized and hosted on **AWS EC2**, using **Nginx** as a reverse proxy and **Gunicorn** as the WSGI server. Static assets are served via **Amazon S3**.

## <footer> Personal Website - Data Projects by [Alejandro Camerlengo](https://www.linkedin.com/in/alejandro-camerlengo/).  Fork it on [GitHub](https://github.com/ale-camer/personal_website) and give it a ⭐! Create issues, too! </footer>
