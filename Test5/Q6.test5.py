import sqlite3
from collections import deque

connection = sqlite3.connect("food_delivery_system.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders(
    Order_ID INTEGER PRIMARY KEY,
    Shop_Name TEXT,
    Delivery_Area TEXT,
    Status TEXT
)
""")

cursor.execute("DELETE FROM Orders")

delivery_records = [
    (201, "Pizza Hut", "Area X", "Waiting"),
    (202, "Dominos", "Area Y", "Waiting"),
    (203, "KFC", "Area Z", "Waiting")
]

cursor.executemany(
    "INSERT INTO Orders VALUES(?,?,?,?)",
    delivery_records
)

connection.commit()

cursor.execute("SELECT * FROM Orders WHERE Status='Waiting'")
waiting_orders = cursor.fetchall()

print("Waiting Deliveries")
for order in waiting_orders:
    print(order)

delivery_map = {
    "Warehouse": ["Area X", "Area Y"],
    "Area X": ["Area Z"],
    "Area Y": [],
    "Area Z": []
}

queue = deque(["Warehouse"])
visited_places = []

while queue:
    current_place = queue.popleft()

    if current_place not in visited_places:
        visited_places.append(current_place)
        queue.extend(delivery_map[current_place])

print("\nDelivery Route")
for place in visited_places:
    print(place)

cursor.execute(
    "UPDATE Orders SET Status='Completed' WHERE Status='Waiting'"
)

connection.commit()

print("\nCompleted Orders")

cursor.execute("SELECT * FROM Orders WHERE Status='Completed'")

for order in cursor.fetchall():
    print(order)

connection.close()
