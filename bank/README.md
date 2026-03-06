# Bank Marketing Prediction Web App

This small Flask app loads a trained model (model/model.pkl) and exposes a form to predict whether a bank customer matches the target criteria.

Quick start (Windows):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Ensure a trained model exists at `model/model.pkl` (a scikit-learn estimator or pipeline saved with `pickle`).

4. Run the app

```powershell
python app.py
```

5. Open http://127.0.0.1:5000 in your browser, fill the form and submit to see the prediction.

Notes:
- The form uses encoded numeric values for categorical fields (job, marital, education). Ensure you use the same encoding used during model training.
- If you want to change secret key, set the `FLASK_SECRET` environment variable.