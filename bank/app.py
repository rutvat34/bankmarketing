from flask import Flask, request, render_template, flash, redirect, url_for
import pickle
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET", "bank-marketing-secret-key")

# Load trained model
model_path = os.path.join("model", "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Model accuracy (you can update this value)
MODEL_ACCURACY = 89.4
# Feature order used by the trained model
FEATURES = [
    'age','job','marital','education','default','balance','housing','loan',
    'contact','day','month','duration','campaign','pdays','previous','poutcome'
]


@app.route('/')
def home():
    return render_template("index.html", accuracy=MODEL_ACCURACY)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/model')
def model_info():
    try:
        model_name = model.__class__.__name__
    except Exception:
        model_name = 'UnknownModel'
    return render_template('model.html', model_name=model_name, accuracy=MODEL_ACCURACY, features=FEATURES)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # GET: show the form page; POST: run prediction
    if request.method == 'GET':
        return render_template('predict.html', accuracy=MODEL_ACCURACY)

    try:
        # Collect all 16 features from form
        age = int(request.form.get('age', ''))
        job = int(request.form.get('job', ''))
        marital = int(request.form.get('marital', ''))
        education = int(request.form.get('education', ''))
        default = int(request.form.get('default', ''))
        balance = float(request.form.get('balance', ''))
        housing = int(request.form.get('housing', ''))
        loan = int(request.form.get('loan', ''))
        contact = int(request.form.get('contact', ''))
        day = int(request.form.get('day', ''))
        month = int(request.form.get('month', ''))
        duration = int(request.form.get('duration', ''))
        campaign = int(request.form.get('campaign', ''))
        pdays = int(request.form.get('pdays', ''))
        previous = int(request.form.get('previous', ''))
        poutcome = int(request.form.get('poutcome', ''))

        # Prepare data for prediction (order matters!)
        data = [[age, job, marital, education, default, balance, housing, loan, contact, day, month, duration, campaign, pdays, previous, poutcome]]

        # Get prediction
        raw_pred = model.predict(data)[0]

        # Compute probability if supported
        probability = None
        try:
            if hasattr(model, 'predict_proba'):
                probability = model.predict_proba(data)[0][1]
        except Exception:
            probability = None

        # Map numeric prediction to human-friendly text
        prediction = "Yes" if int(raw_pred) == 1 else "No"

        return render_template("result.html", prediction=prediction, probability=probability, accuracy=MODEL_ACCURACY)

    except ValueError as e:
        flash("Please fill in all fields with valid numbers.")
        return redirect(url_for('predict'))
    except Exception as e:
        flash(f"Prediction error: {str(e)}")
        return redirect(url_for('predict'))


if __name__ == "__main__":
    app.run(debug=True)
