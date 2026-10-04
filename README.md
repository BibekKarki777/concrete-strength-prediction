# Concrete Strength Prediction System

## Overview
A Django-based university semester project that predicts concrete compressive strength from mixture ingredients and concrete age. It combines a machine learning model with a web interface for making predictions and reviewing results.

## Key Features
- User registration, login, and profile management.
- Strength predictions in megapascals (MPa), with input validation.
- Saved prediction history and visual analytics.
- Staff dashboard for managing users and predictions and viewing model information.
- Responsive interface for desktop and mobile devices.

## Technologies Used
- **Backend:** Python, Django, SQLite.
- **Frontend:** HTML, CSS, JavaScript, Bootstrap, Chart.js.
- **Machine learning:** scikit-learn, pandas, NumPy, joblib.
- **Analysis:** Jupyter Notebook, Matplotlib, Seaborn.

## ML Model and Inputs
The application loads a trained **Random Forest Regressor** from `ml/models/concrete_strength_model.joblib`. The training notebook compares Linear Regression and Random Forest using an 80/20 training/test split.

| Input feature | Unit |
| --- | --- |
| Cement | kg/m³ |
| Blast furnace slag | kg/m³ |
| Fly ash | kg/m³ |
| Water | kg/m³ |
| Superplasticizer | kg/m³ |
| Coarse aggregate | kg/m³ |
| Fine aggregate | kg/m³ |
| Age | days |

The output is concrete compressive strength in **MPa**. Saved evaluation metrics in `model_info.json` are **R²: 0.908**, **MAE: 3.48 MPa**, and **RMSE: 5.25 MPa**.

## Dataset
The included Concrete Compressive Strength dataset is stored at `ml/data/concrete_compressive_strength.csv`. It contains **1,030 records**, eight input features, and the measured compressive strength as the target variable. The analysis and training workflow is available in `ml/notebooks/Concrete_Compressive_Strength_Prediction.ipynb`.

## Project Structure
```text
concrete_strength_system/
├── accounts/          # Authentication and user profiles
├── admin_dashboard/   # Staff dashboard and management
├── config/            # Django settings and main URLs
├── core/              # Home and About pages
├── prediction/        # Prediction forms, model service, and history
├── ml/
│   ├── data/          # Dataset
│   ├── models/        # Trained model and evaluation metrics
│   └── notebooks/     # Analysis and model training
├── static/            # CSS, JavaScript, and images
├── templates/         # HTML templates
├── manage.py
└── requirements.txt
```

## Installation and Setup
Install Python (the existing development environment uses Python 3.13), download or clone the project, and open a terminal in its root directory.

Create and activate a virtual environment in Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate
```

On macOS/Linux, activate it with `source venv/bin/activate` instead.

Install dependencies and initialize the database:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
```

The trained model is included, so retraining is not required. Keep `ml/models/concrete_strength_model.joblib` in place before starting Django.

Optionally, create an administrator account to access the staff dashboard:

```powershell
python manage.py createsuperuser
```

## Run the Django Server
```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ and register or log in to make predictions. Administrator accounts can access the staff dashboard at `/dashboard/` and Django administration at `/admin/`.

## Author
- **Name:** [Bibek Karki]

