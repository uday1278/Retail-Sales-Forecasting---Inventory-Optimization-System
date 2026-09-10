import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from src.feature_engineering import create_features
from src.data_preprocessing import load_and_clean_data


def train_model(df):
    feature_columns = [
        "price",
        "promo",
        "weekday",
        "month",
        "day",
        "year",
        "lag_1",
        "lag_7",
        "rolling_mean_7"
    ]

    X = df[feature_columns]
    y = df["sales_quantity"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("Training model...")

    model = RandomForestRegressor(
        n_estimators=20,
        max_depth=10,
        random_state=42,
        n_jobs=1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    print(f"MAE: {mae:.2f}")

    results = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": predictions
    })

    results.to_csv("outputs/forecast_results.csv", index=False)

    joblib.dump(model, "models/retail_forecast_model.pkl")

    print("Model saved in models/retail_forecast_model.pkl")
    print("Forecast results saved in outputs/forecast_results.csv")

    return model


if __name__ == "__main__":
    df = load_and_clean_data("data/raw/retail_sales.csv")

    df = create_features(df)

    df = df.sample(n=100000, random_state=42)

    print("Using Sample Shape:", df.shape)

    train_model(df)