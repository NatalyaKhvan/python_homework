import sqlite3

# Task 1: Complex JOINs with Aggregation
print("Task 1")

conn = sqlite3.connect("../db/lesson.db")
conn.execute("PRAGMA foreign_keys = 1")
cursor = conn.cursor()

query1 = """
SELECT o.order_id,
    SUM(p.price * li.quantity) AS total_price
FROM orders o
JOIN line_items li ON o.order_id = li.order_id
JOIN products p    ON li.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5
"""
cursor.execute(query1)
results1 = cursor.fetchall()

for order_id, total_price in results1:
    print(f"Order {order_id}: Total Price = {total_price}")

# Task 2: Understanding Subqueries
print("Task 2")

query2 = """
SELECT c.customer_name,
    AVG(order_totals.total_price) AS average_total_price
FROM customers c
LEFT JOIN (
    SELECT o.customer_id AS customer_id_b,
        SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p    ON li.product_id = p.product_id
    GROUP BY o.order_id
) AS order_totals
ON c.customer_id = order_totals.customer_id_b
GROUP BY c.customer_id
ORDER BY c.customer_name
"""
cursor.execute(query2)
results2 = cursor.fetchall()

for customer_name, avg_total in results2:
    print(f"{customer_name}: Average Order Total = {avg_total}")

# Task 3: An Insert Transaction Based on Data
print("Task 3")

try:

    # Get IDs
    cursor.execute(
        "SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'"
    )
    customer_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'"
    )
    employee_id = cursor.fetchone()[0]

    cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
    product_ids = [row[0] for row in cursor.fetchall()]

    # Insert new order
    cursor.execute(
        "INSERT INTO orders (customer_id, employee_id) VALUES (?, ?) RETURNING order_id",
        (customer_id, employee_id),
    )
    order_id = cursor.fetchone()[0]

    # Insert line_items
    for pid in product_ids:
        cursor.execute(
            "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, pid, 10),
        )

    # Commit transaction
    conn.commit()

    # Verify inserted line_items
    cursor.execute(
        """
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?
    """,
        (order_id,),
    )
    results = cursor.fetchall()
    for line_item_id, quantity, product_name in results:
        print(f"Line Item {line_item_id}: {quantity} x {product_name}")

except Exception as e:
    conn.rollback()
    print("Transaction failed:", e)

try:
    # Delete line_items for the inserted order
    cursor.execute("DELETE FROM line_items WHERE order_id = ?", (order_id,))
    # Delete the order itself
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))

    conn.commit()

except Exception as e:
    conn.rollback()
    print("Cleanup failed:", e)

# Task 4: Aggregation with HAVING
print("Task 4")

query4 = """
SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
HAVING COUNT(o.order_id) > 5
"""

cursor.execute(query4)
results4 = cursor.fetchall()

for employee_id, first_name, last_name, order_count in results4:
    print(f"Employee {employee_id}: {first_name} {last_name} - {order_count} orders")

conn.close()
