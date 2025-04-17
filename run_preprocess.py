# === RUN_PREPROCESSING.PY ===

import pandas as pd
import numpy as np
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# === CUSTOMER DATASET ===
df = pd.read_csv("data/raw/Customer_Dataset.csv")
df.drop_duplicates(inplace=True)
df['Name'] = df['Name'].astype(str).str.strip().str.title()
df['Gender'] = df['Gender'].astype(str).str.strip().str.capitalize()
df['City'] = df['City'].astype(str).str.strip().str.title()
df['Age'].fillna(df['Age'].mean(), inplace=True)
df['MonthlySpend'].fillna(df['MonthlySpend'].mean(), inplace=True)

for col in ['Age', 'MonthlySpend']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = np.where(df[col] < lower, lower, np.where(df[col] > upper, upper, df[col]))

numeric_cols = ['Age', 'OrdersPerMonth', 'MonthlySpend', 'SatisfactionScore']
scaled_data = StandardScaler().fit_transform(df[numeric_cols])
scaled_df = pd.DataFrame(scaled_data, columns=[col + "_scaled" for col in numeric_cols])

encoded_df = pd.get_dummies(df[['Gender', 'City']], drop_first=True)

pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_df)
pca_df = pd.DataFrame(pca_data, columns=['PCA1', 'PCA2'])

final_df = pd.concat([df, scaled_df, encoded_df, pca_df], axis=1)

kmeans = KMeans(n_clusters=3, random_state=42)
final_df['Cluster'] = kmeans.fit_predict(final_df[['PCA1', 'PCA2']])
median_spend = final_df['MonthlySpend_scaled'].median()
final_df['HighSpender'] = (final_df['MonthlySpend_scaled'] > median_spend).astype(int)

final_df.to_csv("data/cleaned/Customer_Dataset_Cleaned.csv", index=False)

# === PRODUCT DATASET ===
product_df = pd.read_csv("data/raw/Product_Dataset.csv")
product_df.drop_duplicates(inplace=True)
for col in ['category', 'sub_category', 'brand', 'type']:
    product_df[col] = product_df[col].astype(str).str.strip().str.title()
product_df['rating'] = product_df['rating'].fillna(product_df['rating'].mean())
product_df.dropna(subset=['brand'], inplace=True)
product_df['DiscountPercent'] = np.round(
    ((product_df['market_price'] - product_df['sale_price']) / product_df['market_price']) * 100, 2)
product_df.to_csv("data/cleaned/Product_Dataset_Cleaned.csv", index=False)

# === ORDER TRANSACTIONS ===
order_df = pd.read_csv("data/raw/Order_Transactions.csv")
order_df.drop_duplicates(inplace=True)
for col in ['Product', 'Category', 'Brand', 'PaymentMethod']:
    order_df[col] = order_df[col].astype(str).str.strip().str.title()
order_df['PaymentMethod'] = order_df['PaymentMethod'].fillna("Unknown")
order_df['OrderDate'] = pd.to_datetime(order_df['OrderDate'], errors='coerce')
order_df['OrderMonth'] = order_df['OrderDate'].dt.month
order_df['OrderWeekday'] = order_df['OrderDate'].dt.day_name()
Q1 = order_df['PricePaid'].quantile(0.25)
Q3 = order_df['PricePaid'].quantile(0.75)
IQR = Q3 - Q1
upper_limit = Q3 + 1.5 * IQR
order_df['PricePaid'] = np.where(order_df['PricePaid'] > upper_limit, upper_limit, order_df['PricePaid'])
order_df['UnitPrice'] = order_df['PricePaid'] / order_df['Quantity']
order_df.to_csv("data/cleaned/Order_Transactions_Cleaned.csv", index=False)

# === EXPORT TO SQLITE ===
conn = sqlite3.connect("database/bigbasket_bi.db")
final_df.to_sql("customers", conn, if_exists="replace", index=False)
product_df.to_sql("products", conn, if_exists="replace", index=False)
order_df.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()

print("✅ Data Preprocessing + ML + SQLite Export complete.")
