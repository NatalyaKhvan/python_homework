import pandas as pd
import sqlite3

with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """
        SELECT li.line_item_id, li.quantity, li.product_id, p.product_name, p.price
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
    """
    df = pd.read_sql_query(sql_statement, conn)

print(df.head())

df["total"] = df["quantity"] * df["price"]
print(df.head())

product_summary = (
    df.groupby("product_id")
    .agg(
        count_orders=("line_item_id", "count"),
        total_price=("total", "sum"),
        product_name=("product_name", "first"),
    )
    .reset_index()
)

product_summary = product_summary.sort_values("product_name")
print(product_summary.head())

product_summary.to_csv("order_summary.csv", index=False)
