```bash
├── README.md
├── app.py  # MODULARIZAR!  Tareas:  1. Seguir comentarios agregados en cada funcion. 2. Comentar funciones no comentadas. 3. Todos los comentarios deben estar en ingles y ser simples.  Proximos pasos:  1. agregar un boton para descargarse los datos en keyphrase extraction y seasonality prediction  
├── modules/  # Contain Python modules.
  ├── generate_readme.py  # Generate README.md file. 
  ├── keyphrase_extraction.py  # Contain functions for Keyphrase Extraction functionality. 
  ├── seasonality_prediction.py  # Contain functions for Seasonality Prediction functionality. 
  ├── utils.py  # Custom functions for the projects. 
  ├── whatsapp.py  # Contain functions for WhatsApp functionality. 
  └── world_bank.py  # Contain functions for World Bank functionality. 
├── static/  # Contain static files (CSS, JS and images).
  ├── css/  # Contain CSS main script.
    └── styles.css  # Project Stylesheet File
  ├── images/  # Contain images for the UI.
  ├── js/  # Contain JavaScript scripts.
    ├── base.js  # Project-wise Functionalities
    └── world_bank.js  # World Bank JS Functionalities
  ├── json/
    └── config.json
  ├── seasonality_prediction/  # Contain Seasonality Prediction functionality temporary files.
  └── world_bank/  # Contain World Bank functionality temporary files.
└── templates/  # Contain HTML templates.
  ├── Intro_to_Linear_Algebra_for_Data_Science.html  # Linear Algebra Functionality Template
  ├── Stock_Algorithmic_Trading_Strategy_Backtesting.html  # Algorithmic Trading Functionality Template
  ├── Vector_Norms_Applications_in_Data_Science.html  # Vector Nomrs Functionality Template
  ├── base.html  # Base Project Template
  ├── index.html  # Intro Page Template
  ├── keyphrase_extraction.html  # Keyphrase Extraction Functionality Template
  ├── macro_n_employment_english.html  # Macroeconomic (English) Functionality Template
  ├── macro_n_employment_spanish.html  # Macroeconomic (Spanish) Functionality Template
  ├── mi_cv.html  # Mi CV Functionality Template
  ├── seasonality_prediction.html  # Seasonality Prediction Functionality Template
  ├── trends_in_data_science_labour_market.html  # Trends in Data Science Functionality Template
  ├── whatsapp.html  # WhatsApp Functionality Template
  └── world_bank.html  # World Bank Functionality Template
```