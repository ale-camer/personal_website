# Personal Website - Data Projects

Welcome! I am a data scientist and I've created this website so you can take a look at my resume and have fun with some of my toy projects. This portfolio is designed to showcase ideas and projects that I worked on and to learn a little bit of web development in the process of making the page :)

## Live Demo

You can see the site in action here: [https://personal-website-gz63.onrender.com/](https://personal-website-gz63.onrender.com/)

## Key Features

- Personal portfolio showcasing data projects and my CV.
- Interactive tools for:
  - Extracting keyphrases from text
  - Predicting seasonal trends
  - Analyzing WhatsApp conversations
  - Accessing and visualizing World Bank API data
- Analytical articles and visual insights on:
  - Data science job market trends
  - Macroeconomics
  - Mathematics
  - Algorithmic trading

## Installation

1. Clone the repository: `git clone https://github.com/ale-camer/personal_website.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - On Windows: `venv\Scripts\activate`
   - On Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python main.py`

## Usage

Once the application is running (after step 5 of Installation):
1. Open your web browser and navigate to `http://127.0.0.1:5000/` (or the address shown in your console, typically `http://localhost:PORT` where PORT is specified by your environment, e.g., 5000).
2. Explore the different sections and interactive tools available through the navigation menu.

## Technologies Used

**Frontend**:
- HTML, SCSS, JavaScript

**Backend & Data**:
- Python (Flask, Dash)
- Data manipulation and visualization: pandas, numpy, seaborn, matplotlib, plotly
- Text processing: TextBlob, NLTK, unidecode, regex
- Web and API tools: requests, tqdm, prettytable, folium, branca
- Utility modules and structured programming: dataclasses, abc, os, re, zipfile, time

## Key Files

- `main.py`: Main application script (entry point, configures and runs the Flask app).
- `app.py`: Defines the Flask application instance and core web routes (imported by `main.py`).
- `modules/dash_app.py`: Contains Dash applications for interactive data visualizations.
- `modules/`: Directory for custom Python modules (utilities, text processing, specific functionalities).
- `static/`: Stores static assets (CSS, JavaScript, images) and user-uploaded files.
- `templates/`: Contains HTML templates for the web interface.

## Project Structure

The project directory tree with comments is shown below:

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

## Author

**Alejandro Camerlengo**
- LinkedIn: [https://www.linkedin.com/in/alejandro-camerlengo/](https://www.linkedin.com/in/alejandro-camerlengo/)