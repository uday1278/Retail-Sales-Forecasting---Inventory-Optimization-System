import pandas as pd

def load_and_clean_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Show original size
    print("Original Shape:", df.shape)

    # Rename columns if using Kaggle dataset
    if 'store' in df.columns:
        df.rename(columns={'store': 'store_id'}, inplace=True)

    if 'item' in df.columns:
        df.rename(columns={'item': 'product_id'}, inplace=True)

    if 'sales' in df.columns:
        df.rename(columns={'sales': 'sales_quantity'}, inplace=True)

    # Convert date column into proper format
    df['date'] = pd.to_datetime(df['date'])

    # Remove duplicates and missing values
    df = df.drop_duplicates()
    df = df.dropna()

    # Remove negative sales if any
    df = df[df['sales_quantity'] >= 0]

    print("After Cleaning:", df.shape)
    print("\nColumns:")
    print(df.columns)

    return df


if __name__ == "__main__":
    df = load_and_clean_data("data/raw/retail_sales.csv")

    print("\nFirst 5 Rows:")
    print(df.head())