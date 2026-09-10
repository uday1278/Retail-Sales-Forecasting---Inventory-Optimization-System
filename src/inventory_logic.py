import numpy as np
import pandas as pd
from scipy.stats import norm


def calculate_inventory(forecast, current_stock, lead_time=7, service_level=0.95):
    # Calculate average and standard deviation of forecast
    avg_demand = np.mean(forecast)
    std_demand = np.std(forecast)

    # Z-score based on service level
    z_score = norm.ppf(service_level)

    # Inventory calculations
    safety_stock = z_score * std_demand * np.sqrt(lead_time)
    reorder_point = (avg_demand * lead_time) + safety_stock
    recommended_order = max(0, reorder_point - current_stock)

    return {
        "Average Demand": float(round(avg_demand, 2)),
        "Safety Stock": float(round(safety_stock, 2)),
        "Reorder Point": float(round(reorder_point, 2)),
        "Recommended Order Quantity": float(round(recommended_order, 2))
    }


if __name__ == "__main__":
    # Example predicted sales for the next 7 days
    sample_forecast = [42, 45, 43, 47, 44, 46, 48]

    # Assume current stock available
    current_stock = 150

    result = calculate_inventory(
        forecast=sample_forecast,
        current_stock=current_stock
    )

    print("\nInventory Recommendation:")
    print(result)

    # Save recommendation to CSV
    recommendation_df = pd.DataFrame([result])

    recommendation_df.to_csv(
        "outputs/inventory_recommendations.csv",
        index=False
    )

    print("\nSaved to outputs/inventory_recommendations.csv")