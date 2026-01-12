# ⚡ Smart Home Energy Consumption Forecasting

A Flask-based web application that predicts **future energy consumption** for smart home devices using a **deep learning time-series model**.  

---

## 🚀 What This Does

- Predicts **energy usage over time** for a selected smart device  
- Supports multiple prediction ranges:
  - **Next 24 hours**
  - **Next 7 days**
  - **Next 30 days**
- Uses historical data + temporal context to forecast future consumption
- Displays predictions alongside **timestamps**

---

## 🧠 Model Overview

- **Architecture**: Sequence-based deep learning model (trained on sliding windows)
- **Training shape**: (x, 12, 30)
- `12` → timesteps per sequence  
- `30` → engineered features per timestep

- **Custom loss function**: `asymmetric_huber`
- Penalizes under-predictions more than over-predictions

---

## 🏗️ Tech Stack

### Backend
- Flask
- TensorFlow / Keras
- Pandas, NumPy
- scikit-learn
- joblib

### ML Pipeline
- OneHotEncoder (categorical features)
- MinMaxScaler (numerical features)
- Preprocessing artifacts saved and reused at inference

### Frontend
- Jinja2 templates
- Bootstrap component for responsiveness
- CSS handled separately

---

## 📁 Project Structure
**pending**


---

## 🧩 Features Used by the Model

### Binary / Integer
- `user_present`
- `status`
- `is_weekend`
- `hour_of_day`
- `day_of_week`
- `month_of_year`

### Numerical
- `indoor_temp`
- `outdoor_temp`
- `humidity`
- `light_level`
- Rolling energy statistics
- Lag features (`1H`, `1D`, `1W`)

### Categorical (One-Hot Encoded)
- `device_type`
- `room`
- `activity`

All features are **forced to match training dtypes** during inference.

---

## 🔮 Prediction Flow

1. User selects:
   - Home ID
   - Device type
   - Prediction range
2. App:
   - Generates future timestamps
   - Reuses last known categorical and numerical values
   - Builds temporal features
   - Applies saved encoders and scalers
   - Reshapes into `(1, n_steps, features)`
3. Model predicts energy consumption
4. Results displayed as: (charts coming soon)
