import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------

single_file_acc = pd.read_csv(r"V:\tracking-barbell-exercises\data\raw\MetaMotion\A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")
single_file_gyr = pd.read_csv(r"V:\tracking-barbell-exercises\data\raw\MetaMotion\A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files = glob(r"V:\tracking-barbell-exercises\data\raw\MetaMotion\*.csv")
len(files)

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
data_path = "../../data/raw/MetaMotion"
f = files[1]

participant = f.split("-")[2][-1].replace(data_path,"")
label = f.split("-")[3]
category = f.split("-")[4].rstrip("12345")
print(category , label , participant)


df = pd.read_csv(f)
print(df)
df["participant"] = participant
df["label"] = label
df["category"] = category

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------

acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

acc_set = 1
gyr_set = 1

for f in files:
    participant = f.split("-")[2][-1].replace(data_path,"")
    label = f.split("-")[3]
    category = f.split("-")[4].rstrip("12345").rstrip("_MetaWear_2019")
    
    df = pd.read_csv(f)
    
    df["participant"] = participant
    df["label"] = label
    df["category"] = category
    
    if "Accelerometer" in f :
        df["set"] = acc_set
        acc_set += 1
        acc_df = pd.concat([acc_df , df])
    
    if "Gyroscope" in f :
        df["set"] = gyr_set
        gyr_set += 1
        gyr_df = pd.concat([gyr_df , df])
print(gyr_df)
print(acc_df)
acc_df[acc_df["set"] == 10]
    
# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------

acc_df.info()

pd.to_datetime(df["epoch (ms)"], unit="ms")
# pd.to_datetime(df["time (01:00)"]).dt.month
# df["time (01:00)"]

acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

del acc_df["epoch (ms)"]
del acc_df["time (01:00)"]
del acc_df["elapsed (s)"]

del gyr_df["epoch (ms)"]
del gyr_df["time (01:00)"]
del gyr_df["elapsed (s)"]


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
files = glob(r"V:\tracking-barbell-exercises\data\raw\MetaMotion\*.csv")

def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for f in files:
        participant = f.split("-")[2][-1].replace(data_path,"")
        label = f.split("-")[3]
        category = f.split("-")[4].rstrip("12345").rstrip("_MetaWear_2019")
        
        df = pd.read_csv(f)
        
        df["participant"] = participant
        df["label"] = label
        df["category"] = category
        
        if "Accelerometer" in f :
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df , df])
        
        if "Gyroscope" in f :
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df , df])
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]
    
    return acc_df,gyr_df

acc_df , gyr_df = read_data_from_files(files)
print (acc_df,gyr_df)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------

data_merged = pd.concat([acc_df.iloc[:,:3],gyr_df] , axis=1)
data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "participant",
    "label",
    "category",
    "set" 
]

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ -> measuring 0.04sec
# Gyroscope:        25.000Hz -> measuring 0.08sec

sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "participant": "last",
    "label": "last",
    "category": "last",
    "set": "last" 
}


# data_merged[:1000].resample(rule="200ms").mean().apply(sampling)

days = [g for n , g in data_merged.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat([df.resample(rule="200ms").apply(sampling).dropna() for df in days])

data_resampled.info()
data_resampled["set"] = data_resampled["set"].astype("int")
data_resampled.info()


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle(r"V:\tracking-barbell-exercises\data\interim\01_data_processed.pkl")