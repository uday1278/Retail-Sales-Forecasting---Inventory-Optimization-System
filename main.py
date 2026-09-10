from src.data_preprocessing import load_and_clean_data
from src.feature_engineering import create_features
from src.train_model import train_model

print("Step 1: Loading Data...")
df = load_and_clean_data("data/raw/retail_sales.csv")

print("\nStep 2: Creating Features...")
df = create_features(df)

# Use smaller sample for faster execution
df = df.sample(n=100000, random_state=42)

print("\nStep 3: Training Model...")
train_model(df)

print("\nProject Completed Successfully!")