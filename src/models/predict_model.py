import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter
from scipy.signal import argrelextrema
from sklearn.metrics import mean_absolute_error

# Load Data
def load_data(filepath):
    df = pd.read_pickle(filepath)
    df = df[df["label"] != "rest"]

    # Calculate magnitude of accelerometer and gyroscope signals
    df["acc_r"] = np.sqrt(df["acc_x"] ** 2 + df["acc_y"] ** 2 + df["acc_z"] ** 2)
    df["gyr_r"] = np.sqrt(df["gyr_x"] ** 2 + df["gyr_y"] ** 2 + df["gyr_z"] ** 2)
    
    return df

# Count Repetitions
def count_reps(dataset, low_pass_filter, fs, cutoff=0.4, order=10, column="acc_r"):
    filtered_data = low_pass_filter.low_pass_filter(
        dataset, col=column, sampling_frequency=fs, cutoff_frequency=cutoff, order=order
    )

    # Detect peaks
    indexes = argrelextrema(filtered_data[column + "_lowpass"].values, np.greater)
    peaks = filtered_data.iloc[indexes]

    # Plot results
    plt.figure(figsize=(12, 4))
    plt.plot(filtered_data[f"{column}_lowpass"], label="Filtered Signal")
    plt.scatter(peaks.index, peaks[f"{column}_lowpass"], color="red", label="Peaks")
    plt.title(f"Repetition Count: {len(peaks)}")
    plt.xlabel("Time")
    plt.ylabel(f"{column}_lowpass")
    plt.legend()
    plt.show()

    return len(peaks)

# Predict Repetitions for All Sets
def predict_reps(df, low_pass_filter, fs):
    df["reps"] = df["category"].apply(lambda x: 5 if x == "heavy" else 10)
    rep_df = df.groupby(["label", "category", "set"])["reps"].max().reset_index()
    rep_df["reps_pred"] = 0

    for s in df["set"].unique():
        subset = df[df["set"] == s]
        column, cutoff = "acc_r", 0.4

        # Exercise-specific settings
        if subset["label"].iloc[0] == "squat":
            cutoff = 0.35
        elif subset["label"].iloc[0] == "row":
            cutoff = 0.65
            column = "gyr_x"
        elif subset["label"].iloc[0] == "ohp":
            cutoff = 0.35

        # Predict repetitions
        reps = count_reps(subset, low_pass_filter, fs, cutoff=cutoff, column=column)
        rep_df.loc[rep_df["set"] == s, "reps_pred"] = reps

    return rep_df

# Evaluate Model
def evaluate_model(rep_df):
    error = mean_absolute_error(rep_df["reps"], rep_df["reps_pred"])
    print(f"Mean Absolute Error: {error:.2f}")

    # Bar plot of actual vs predicted reps
    rep_df.groupby(["label", "category"])[["reps", "reps_pred"]].mean().plot.bar()
    plt.title("Actual vs Predicted Repetitions")
    plt.ylabel("Repetitions")
    plt.show()

# Main Execution
def main():
    filepath = "../../data/interim/01_data_processed.pkl"
    df = load_data(filepath)

    fs = 1000 / 200  # Sampling frequency
    low_pass_filter = LowPassFilter()

    # Predict repetitions
    rep_df = predict_reps(df, low_pass_filter, fs)

    # Evaluate results
    evaluate_model(rep_df)

if __name__ == "__main__":
    main()
