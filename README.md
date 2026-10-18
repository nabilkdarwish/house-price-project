# House Price Prediction

An end-to-end machine-learning web app for estimating residential property prices from listing details. The project brings together a data-preparation notebook, a scikit-learn regression pipeline, a FastAPI prediction service, and a React + TypeScript interface.

> **Learning project:** the bundled example data is synthetic. The reported metrics are for that synthetic dataset and should not be used to value real property. Replace it with the linked real dataset and retrain before drawing conclusions.

## What it includes

- A Jupyter notebook for data cleaning, feature engineering, model comparison, evaluation, and pipeline export.
- A FastAPI service with GET /health and validated POST /predict endpoints.
- A React + TypeScript form that collects property details and displays the estimate returned by the API.
- Example configuration files, a Dockerfile for the API, and backend prediction tests.

## Architecture

1. Prepare the dataset and train the model in house-price-project/notebooks/.
2. Export the fitted scikit-learn pipeline and supporting location and metric files.
3. Load the pipeline in the FastAPI backend and request a prediction.
4. Submit property details from the frontend and show the returned estimate.

## Run locally

See the [full project guide](house-price-project/README.md) for dataset preparation, API details, model methodology, and troubleshooting. Start the API and frontend in separate terminals.

### API

```bash
cd house-price-project/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The interactive API docs are available at http://localhost:8000/docs.

### Frontend

```bash
cd house-price-project/frontend
npm install
cp .env.example .env
npm run dev
```

The frontend expects the API at http://localhost:8000 by default. Configure VITE_API_BASE_URL in frontend/.env if your API runs elsewhere.

### Train the model

The notebook and synthetic-data generator are in house-price-project/notebooks/. Follow the setup in the [full guide](house-price-project/README.md). To evaluate on real listings, obtain the dataset from the source linked there, replace the synthetic input, and rerun the notebook.

## Data and limitations

This is a portfolio and learning prototype, not a real-estate appraisal service. Synthetic examples cannot establish real-world accuracy. The dataset source, preprocessing choices, split, cross-validation, and reported metrics are documented in the full guide; performance may vary substantially with real data, location, time period, and listing quality.

## Technology

Python · pandas · NumPy · scikit-learn · Jupyter · FastAPI · Pydantic · React · TypeScript · Vite

## Repository layout

```text
house-price-project/
├── backend/    # FastAPI service, model files, tests, Dockerfile
├── frontend/   # React + TypeScript app
└── notebooks/  # data generator and model-training notebook
```

Created by [Nabil Khaled Darwish](https://github.com/nabilkdarwish).
