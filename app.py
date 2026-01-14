from flask import Flask, render_template, request, session
import pandas as pd
import tensorflow as tf
import os
from dotenv import load_dotenv
from pipeline.custom_loss import asymmetric_huber
from pipeline.inference import make_input_seq
from pipeline.aggregation import aggregate_predictions
from utils.smart_tip import generate_smart_tip

load_dotenv()

model = tf.keras.models.load_model("./models/FinalModel.keras", custom_objects={"asymmetric_huber": asymmetric_huber}
)

df = pd.read_csv("./database/sample.csv")

PRED_RANGE_TO_STEPS = {
    "24h_hourly": (24 * 4),
    "7d_daily": (7 * 24 * 4),
    "30d_monthly": (30 * 24 * 4)
}

AGG_MAP = {
    "24h_hourly": ["hourly"],
    "7d_daily": ["daily"],
    "30d_monthly": ["daily", "weekly"]
}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        home_id = request.form['home_id']
        print(f"Logged in with Home ID: {home_id}")
        session['home_id'] = int(home_id)  
        session['logged_in'] = True
    return render_template('main.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    if request.method == 'POST':
        device_types = request.form.getlist('device_type[]')
        pred_range = request.form['prediction_range']
        
        print(f"Device: {device_types}, Range: {pred_range}")

        n_steps = PRED_RANGE_TO_STEPS[pred_range]
        
        X = make_input_seq(df, home_id=session['home_id'], device_types=device_types,
        n_steps=n_steps)

        y_pred = model.predict(X).flatten()

        pred_by_device = {}

        idx = 0
        for device in device_types:
            pred_by_device[device] = y_pred[idx: idx + n_steps].tolist()
            idx += n_steps

        agg_modes = AGG_MAP[pred_range]
        series = {}

        for device, preds in pred_by_device.items():
            series[device] = {}

            for mode in agg_modes:
                series[device][mode] = aggregate_predictions(preds, mode).tolist()


        per_device_totals = {
            device: sum(preds)
            for device, preds in pred_by_device.items()
        }

        total_energy = sum(per_device_totals.values())

        print()
        print()
        print(per_device_totals)
        print()
        print()

        dashboard = {
            "metadata": {
                "devices": device_types,
                "range": pred_range
            },
            "kpis":{
                "total_energy": round(total_energy, 2),
                "per_device": per_device_totals
            },
            "series": series,
            "smartTip": generate_smart_tip(per_device_totals)
        }

        return render_template("main.html", dashboard=dashboard)


if __name__ == '__main__':
    app.run(debug=True)