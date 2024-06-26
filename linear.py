# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load and preprocess the sales data
data = pd.read_csv(r"D:/IBM PROJECT/productsalesanalysis.csv")

# Select the features and target variable
X = data[['Product_Name', 'Region', 'Customer_Segment', 'Product_Category', 'Product_Sub-Category', 'Sales', 'Product_Container', 'Ship_Mode']]
Y = data['Profit']

# Specify which features are categorical
categorical_features = ['Product_Name', 'Region', 'Customer_Segment', 'Product_Category', 'Product_Sub-Category', 'Product_Container', 'Ship_Mode']

# One-hot encode categorical features
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), categorical_features)], remainder='passthrough')
X = ct.fit_transform(X)

# Avoiding the dummy variable trap by dropping one column for each one-hot encoded feature
X = X[:, 1:]

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, Y_train)

# Ask the user for input: Region
region_input = input("Enter a Region: ")

# Filter the dataset for the specified region
filtered_data = data[data['Region'] == region_input]

# If there are no records for the specified region, inform the user
if filtered_data.shape[0] == 0:
    print("No records found for the specified region.")
else:
    # Use the model to predict profit for the filtered data
    X_filtered = filtered_data[['Product_Name', 'Region', 'Customer_Segment', 'Product_Category', 'Product_Sub-Category', 'Sales', 'Product_Container', 'Ship_Mode']]
    X_filtered = ct.transform(X_filtered)
    X_filtered = X_filtered[:, 1:]
    y_pred_filtered = model.predict(X_filtered)

    # Sort the filtered data by predicted profit in descending order
    sorted_data = filtered_data.copy()
    sorted_data['Predicted_Profit'] = y_pred_filtered
    sorted_data = sorted_data.sort_values(by='Predicted_Profit', ascending=False)

    # Get the top 5 and bottom 5 records
    top_5 = sorted_data.head(5)
    bottom_5 = sorted_data.tail(5)

    # Print the top 5 predicted profit values and corresponding Order_IDs, Product Names
    print("\nTop 5 Predicted Profit Values:")
    for index, row in top_5.iterrows():
        print(f"Order_ID: {row['Order_ID']}, Product Name: {row['Product_Name']}, Predicted Profit: {row['Predicted_Profit']:.2f}")

    # Print the bottom 5 predicted profit values and corresponding Order_IDs, Product Names
    print("\nBottom 5 Predicted Profit Values:")
    for index, row in bottom_5.iterrows():
        print(f"Order_ID: {row['Order_ID']}, Product Name: {row['Product_Name']}, Predicted Profit: {row['Predicted_Profit']:.2f}")

    # Create a scatter plot for visualization
    plt.figure(figsize=(8, 6))
    plt.scatter(filtered_data['Profit'], y_pred_filtered, color='blue', marker='o')
    plt.title('Actual vs. Predicted Profit for the Specified Region')
    plt.xlabel('Actual Profit')
    plt.ylabel('Predicted Profit')

    # Add a diagonal line for reference (perfect predictions)
    plt.plot([filtered_data['Profit'].min(), filtered_data['Profit'].max()], [filtered_data['Profit'].min(), filtered_data['Profit'].max()], 'k--', lw=2)

    # Show the plot
    plt.show()