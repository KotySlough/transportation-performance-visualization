import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_and_visualize_carrier_performance(filepath):
    """
    Analyzes carrier shipping data and generates visualizations for performance metrics.

    Args:
        filepath (str): The path to the shipping data CSV file.
    """
    # --- 1. Data Loading and Preparation ---
    print("Loading data...")
    try:
        # Load the dataset
        df = pd.read_csv(filepath)

        # Convert date columns to datetime objects
        df['ship_date'] = pd.to_datetime(df['ship_date'])
        df['delivery_date'] = pd.to_datetime(df['delivery_date'])
        df['planned_delivery_date'] = pd.to_datetime(df['planned_delivery_date'])
    except FileNotFoundError:
        print(f"Error: The file was not found at {filepath}")
        return
    except KeyError as e:
        print(f"Error: A required column is missing from the CSV file: {e}")
        return


    print("Data loaded successfully. Starting analysis...")

    # --- 2. Feature Engineering ---
    # Calculate delay in days
    df['delay_days'] = (df['delivery_date'] - df['planned_delivery_date']).dt.days

    # Identify if a shipment was on time (delay <= 0)
    df['on_time'] = df['delay_days'] <= 0

    # Extract the month from the ship date for trend analysis
    df['shipment_month'] = df['ship_date'].dt.to_period('M')

    # --- 3. Carrier Performance Calculation ---
    # Calculate on-time percentage per carrier
    on_time_performance = df.groupby('carrier_name')['on_time'].mean().sort_values(ascending=False) * 100

    # Calculate average delay for LATE shipments only
    late_shipments = df[df['on_time'] == False]
    
    # Check if there are any late shipments before calculating average delay
    if not late_shipments.empty:
        average_delay = late_shipments.groupby('carrier_name')['delay_days'].mean().sort_values(ascending=True)
    else:
        average_delay = pd.Series() # Create an empty series if no late shipments


    # Calculate total shipments per month
    shipments_per_month = df.groupby('shipment_month').size()
    shipments_per_month.index = shipments_per_month.index.to_timestamp() # Convert PeriodIndex to DatetimeIndex for plotting

    print("Analysis complete. Generating visualizations...")

    # --- 4. Data Visualization ---
    # Set a professional style for the plots
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))

    # Plot 1: On-Time Delivery Percentage by Carrier
    on_time_plot = sns.barplot(x=on_time_performance.index, y=on_time_performance.values, palette="viridis")
    on_time_plot.set_title('On-Time Delivery Percentage by Carrier', fontsize=16, fontweight='bold')
    on_time_plot.set_xlabel('Carrier', fontsize=12)
    on_time_plot.set_ylabel('On-Time Percentage (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    plt.savefig('on_time_delivery_percentage.png')
    print("Saved 'on_time_delivery_percentage.png'")
    plt.close() # Close the plot to prepare for the next one

    # Plot 2: Average Delay Days for Late Shipments by Carrier (only if there is data)
    if not average_delay.empty:
        plt.figure(figsize=(10, 6))
        avg_delay_plot = sns.barplot(x=average_delay.index, y=average_delay.values, palette="plasma")
        avg_delay_plot.set_title('Average Delay (in Days) for Late Shipments', fontsize=16, fontweight='bold')
        avg_delay_plot.set_xlabel('Carrier', fontsize=12)
        avg_delay_plot.set_ylabel('Average Delay (Days)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('average_carrier_delays.png')
        print("Saved 'average_carrier_delays.png'")
        plt.close()
    else:
        print("Skipping 'Average Delay' plot because there were no late shipments.")

    # Plot 3: Total Shipments Over Time
    plt.figure(figsize=(12, 6))
    shipments_trend_plot = sns.lineplot(x=shipments_per_month.index, y=shipments_per_month.values, marker='o', color='royalblue')
    shipments_trend_plot.set_title('Total Shipments per Month', fontsize=16, fontweight='bold')
    shipments_trend_plot.set_xlabel('Month', fontsize=12)
    shipments_trend_plot.set_ylabel('Number of Shipments', fontsize=12)
    plt.tight_layout()
    plt.savefig('monthly_shipment_trends.png')
    print("Saved 'monthly_shipment_trends.png'")
    plt.close()

    print("\nVisualizations have been generated and saved as PNG files in your project folder.")


# --- Main Execution Block ---
# This is the standard way to make a Python script runnable.
# It ensures the code inside only runs when you execute the file directly.
if __name__ == "__main__":
    # Define the path to the CSV file
    csv_file = 'carrier_performance_data_viz.csv'

    # Run the analysis function
    analyze_and_visualize_carrier_performance(csv_file)
