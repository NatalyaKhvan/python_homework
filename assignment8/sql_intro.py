import sqlite3

with sqlite3.connect("../db/magazines.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    # Create tables
    try:
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            publisher_id INTEGER,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id)
        )
        """
        )

    except sqlite3.Error as e:
        print(e)

    # Helper to check existence
    def exists(table, where_clause, params):
        cursor.execute(f"SELECT 1 FROM {table} WHERE {where_clause}", params)
        return cursor.fetchone() is not None

    # Data functions
    def add_publisher(name):
        if not exists("publishers", "name = ?", (name,)):
            cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))

    def add_magazine(name, publisher_name):
        cursor.execute(
            "SELECT publisher_id FROM publishers WHERE name = ?", (publisher_name,)
        )
        publisher = cursor.fetchone()
        if publisher and not exists("magazines", "name = ?", (name,)):
            cursor.execute(
                "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
                (name, publisher[0]),
            )

    def add_subscriber(name, address):
        if not exists("subscribers", "name = ? AND address = ?", (name, address)):
            cursor.execute(
                "INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address)
            )

    def add_subscription(sub_name, sub_address, mag_name, exp_date):
        cursor.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (sub_name, sub_address),
        )
        sub = cursor.fetchone()
        cursor.execute("SELECT magazine_id FROM magazines WHERE name = ?", (mag_name,))
        mag = cursor.fetchone()
        if (
            sub
            and mag
            and not exists(
                "subscriptions",
                "subscriber_id = ? AND magazine_id = ?",
                (sub[0], mag[0]),
            )
        ):
            cursor.execute(
                "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
                (sub[0], mag[0], exp_date),
            )

    # Populate tables
    for name in ["Time Inc.", "Meredith Corp.", "National Geographic Society"]:
        add_publisher(name)

    add_magazine("Time", "Time Inc.")
    add_magazine("Real Simple", "Meredith Corp.")
    add_magazine("National Geographic", "National Geographic Society")

    add_subscriber("Katy Smith", "123 Main St")
    add_subscriber("John Jackson", "456 Oak Ave")
    add_subscriber("Ann Clark", "789 Pine Rd")

    add_subscription("Katy Smith", "123 Main St", "Time", "2025-12-31")
    add_subscription("John Jackson", "456 Oak Ave", "Real Simple", "2025-06-30")
    add_subscription("Ann Clark", "789 Pine Rd", "National Geographic", "2026-01-15")

    conn.commit()
    print("Database created and populated successfully!")

    # SQL Queries
    # SQL Queries helper
    def run_query(title, query, params=()):
        print(f"\n{title}")
        cursor.execute(query, params)
        for row in cursor.fetchall():
            print(row)

    # All information from the subscribers table
    run_query("All magazines sorted by name:", "SELECT * FROM magazines ORDER BY name")

    # All magazines sorted by name
    print("\nAll magazines sorted by name:")
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    for row in cursor.fetchall():
        print(row)

    # Magazines for a particular publisher (example: 'Meredith Corp.')
    publisher_name = "Meredith Corp."
    run_query(
        f"Magazines published by {publisher_name}:",
        "SELECT m.magazine_id, m.name, p.name FROM magazines m "
        "JOIN publishers p ON m.publisher_id = p.publisher_id "
        "WHERE p.name = ?",
        (publisher_name,),
    )
