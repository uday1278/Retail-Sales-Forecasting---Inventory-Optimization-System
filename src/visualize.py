import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv("outputs/forecast_results.csv")

print(results.head())

plt.figure(figsize=(12, 6))

plt.plot(
    results["Actual"][:100],
    label="Actual Sales"
)

plt.plot(
    results["Predicted"][:100],
    label="Predicted Sales"
)

plt.title("Actual vs Predicted Sales")
plt.xlabel("Data Points")
plt.ylabel("Sales Quantity")
plt.legend()
plt.grid(True)

plt.savefig("images/actual_vs_predicted.png")

print("Graph saved successfully in images/actual_vs_predicted.png")