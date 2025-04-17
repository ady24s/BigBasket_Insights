# === RUN_EDA.PY ===

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
output_dir = "static/outputs"
os.makedirs(output_dir, exist_ok=True)

# === CUSTOMER DATASET ===
df = pd.read_csv("data/cleaned/Customer_Dataset_Cleaned.csv")
sns.countplot(data=df, x='Gender')
plt.title("Gender Distribution")
plt.savefig(f"{output_dir}/gender_distribution.png")
plt.clf()

sns.boxplot(data=df, x='Gender', y='MonthlySpend')
plt.title("Monthly Spend by Gender")
plt.savefig(f"{output_dir}/spend_by_gender.png")
plt.clf()

sns.heatmap(df[['Age', 'OrdersPerMonth', 'MonthlySpend', 'SatisfactionScore']].corr(), annot=True, cmap='YlOrBr')
plt.title("Customer Correlation Heatmap")
plt.savefig(f"{output_dir}/customer_corr_heatmap.png")
plt.clf()

# === PRODUCT DATASET ===
df = pd.read_csv("data/cleaned/Product_Dataset_Cleaned.csv")
sns.histplot(df['DiscountPercent'], bins=30, kde=True)
plt.title("Distribution of Discounts (%)")
plt.savefig(f"{output_dir}/discount_distribution.png")
plt.clf()

sns.histplot(df['rating'], bins=10, kde=True)
plt.title("Rating Distribution")
plt.savefig(f"{output_dir}/rating_distribution.png")
plt.clf()

# === ORDER TRANSACTIONS DATASET ===
df = pd.read_csv("data/cleaned/Order_Transactions_Cleaned.csv")
sns.countplot(x='OrderWeekday', data=df, order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
plt.title("Orders by Weekday")
plt.savefig(f"{output_dir}/orders_by_weekday.png")
plt.clf()

sns.scatterplot(x='Quantity', y='PricePaid', data=df)
plt.title("Quantity vs. PricePaid")
plt.savefig(f"{output_dir}/quantity_vs_price.png")
plt.clf()

sns.boxplot(data=df, x='PaymentMethod', y='UnitPrice')
plt.title("Unit Price by Payment Method")
plt.xticks(rotation=45)
plt.savefig(f"{output_dir}/unitprice_by_paymentmethod.png")
plt.clf()

print("✅ EDA complete. Charts saved in static/outputs/")
