# Quantify Motion - Exercise Repetition Detection using Sensor Data

Quantify Motion is a machine learning-powered system that accurately detects and counts repetitions of strength-based exercises using sensor data from accelerometers and gyroscopes.

---

## 🚀 Project Objective

To automate the process of exercise repetition counting by analyzing motion sensor data (accelerometer + gyroscope) collected during workouts. The system targets key exercises like Bench Press, Squats, Deadlifts, Rows, and Overhead Press (OHP).

---

## 🧠 Core Features

- **Sensor-Based Input**: Uses data from accelerometer and gyroscope.
- **Preprocessing Pipeline**: Noise reduction using low-pass filtering.
- **Feature Extraction**: Magnitude signal calculation, peak detection, repetition counting.
- **Performance Evaluation**: Uses Mean Absolute Error (MAE) to measure accuracy.

---

## 🧪 Technologies Used

- Python 🐍
- NumPy
- Pandas
- SciPy
- Matplotlib
- Scikit-learn

---

## 📊 Dataset

The dataset is manually collected using mobile or wearable sensors. Each row contains:
- Timestamp
- Acceleration (x, y, z)
- Gyroscope (x, y, z)
- Exercise label (Bench Press, Squat, etc.)

---

## 🔁 Workflow

1. **Data Collection**
2. **Signal Preprocessing**
   - Low-pass filtering
   - Smoothing
3. **Feature Engineering**
   - Magnitude calculation
4. **Peak Detection**
   - Using thresholds and spacing
5. **Repetition Count**
   - Count peaks as reps
6. **Evaluation**
   - Compare with actual count using MAE

---

## 📈 Sample Results

| Exercise       | Actual Reps | Detected Reps | MAE |
|----------------|-------------|---------------|-----|
| Bench Press    | 10          | 9             | 1.0 |
| Squats         | 15          | 14            | 1.0 |
| Deadlifts      | 12          | 12            | 0.0 |

---

## 📂 Project Structure




---

## 🔮 Future Improvements

- Real-time repetition feedback using mobile app
- Pose estimation integration
- Support for free-form workouts and noisy environments
- Expand dataset diversity

---

## 📬 Contact

Made with 💪 by Vishal Kumar Gautam  
[LinkedIn](https://www.linkedin.com/in/vishal0115/) | [GitHub](https://github.com/VishalPSIT)

