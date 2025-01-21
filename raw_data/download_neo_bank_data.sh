#!/bin/bash

# Set the target directory 
TARGET_DIR="./raw_data"

# Download the dataset using Kaggle API into the current directory
kaggle competitions download -c neo-bank-non-sub-churn-prediction -p "$TARGET_DIR"

echo "Download complete. Data saved to $TARGET_DIR"
