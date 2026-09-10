import pandas as pd
from src.data_preprocessing import load_and_clean_data


def create_features(df):
    # Sort data by item and date
    df = df.sort_values(by=["item_id", "date"])

    # Lag features
    df["lag_1"] = df.groupby("item_id")["sales_quantity"].shift(1)
    df["lag_7"] = df.groupby("item_id")["sales_quantity"].shift(7)

    # Rolling mean feature
    df["rolling_mean_7"] = (
        df.groupby("item_id")["sales_quantity"]
        .shift(1)
        .rolling(window=7)
        .mean()
    )

    # Additional date features
    df["day"] = df["date"].dt.day
    df["year"] = df["date"].dt.year

    # Remove rows with missing lag values
    df = df.dropna()

    return df


if __name__ == "__main__":
    df = load_and_clean_data("data/raw/retail_sales.csv")

    df = create_features(df)

    print(df[[
        "date",
        "item_id",
        "sales_quantity",
        "lag_1",
        "lag_7",
        "rolling_mean_7"
    ]].head())

    print("\nNew Shape:", df.shape)