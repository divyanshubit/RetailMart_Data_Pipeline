import pandas as pd
import numpy as np
import sqlite3

def run_pipeline():
    print("Pipeline started")


    sales_df = pd.read_csv("sales.csv")
    products_df = pd.read_csv("products.csv")
    stores_df = pd.read_csv("stores.csv")

    print("Sales Data Shape:", sales_df.shape)
    print("Products Data Shape:", products_df.shape)
    print("Stores Data Shape:", stores_df.shape)

    print(sales_df.head())
    print(products_df.head())
    print(stores_df.head())

    print("\nMissing values in Sales Data:")
    print(sales_df.isnull().sum())

    print("\nMissing values in Products Data:")
    print(products_df.isnull().sum())

    print("\nMissing values in Stores Data:")
    print(stores_df.isnull().sum())

    duplicates = sales_df.duplicated().sum()
    print("Duplicate rows:", duplicates)

    sales_df = sales_df.drop_duplicates()
    print("Shape after removing duplicates:", sales_df.shape)

    sales_df['quantity'] = sales_df['quantity'].fillna(0)

    sales_df = sales_df.dropna(subset=['amount'])
    print("Cleaned Data Shape:", sales_df.shape)

    sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
    sales_df['amount'] = sales_df['amount'].astype(float)
    print(sales_df.dtypes)
    final_df = pd.merge(sales_df, products_df, on='product_id', how='inner')
    final_df = pd.merge(final_df, stores_df, on='store_id', how='inner')
    print(final_df.head())
    print(final_df.shape)
    final_df['total_revenue'] = final_df['quantity'] * final_df['price']
    print("Mean Revenue:", final_df['total_revenue'].mean())
    print("Max Revenue:", final_df['total_revenue'].max())
    print("Min Revenue:", final_df['total_revenue'].min())
    city_revenue = final_df.groupby('city')['total_revenue'].sum().sort_values(ascending=False)

    print(city_revenue)

    conn = sqlite3.connect("retail_sales.db")

    final_df.to_sql(
        "retail_sales",
        conn,
        if_exists="replace",
        index=False
    )

    query = """
    SELECT product_name,
        SUM(quantity) as total_quantity
    FROM retail_sales
    GROUP BY product_name
    ORDER BY total_quantity DESC
    LIMIT 3;
    """

    top_products = pd.read_sql_query(query, conn)

    print(top_products)

    query = """
    SELECT store_name,
        sale_date,
        SUM(total_revenue) as revenue
    FROM retail_sales
    GROUP BY store_name, sale_date
    ORDER BY revenue DESC;
    """

    store_revenue = pd.read_sql_query(query, conn)

    print(store_revenue)

    print("Total Transactions:", len(final_df))
    print("Total Revenue:", final_df['total_revenue'].sum())

    top_city = city_revenue.idxmax()
    print("Top Selling City:", top_city)

    top_product = final_df.groupby('product_name')['quantity'].sum().idxmax()
    print("Top Selling Product:", top_product)
    conn.close()
    print("Pipeline completed successfully")

try:
    run_pipeline()
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print("Error:", e)