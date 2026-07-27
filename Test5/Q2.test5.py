import sqlite3
import heapq

conn = sqlite3.connect("hospital.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Patients(
id INTEGER PRIMARY KEY,
name TEXT,
age INTEGER,
priority INTEGER
)
""")

cur.execute("DELETE FROM Patients")

data = [
    (101,"Rahul",25,3),
    (102,"Priya",40,1),
    (103,"Arjun",60,2),
    (104,"Sneha",30,4),
    (105,"Ramesh",50,1)
]

cur.executemany("INSERT INTO Patients VALUES(?,?,?,?)", data)
conn.commit()

class Patient:
    def __init__(self,id,name,age,priority):
        self.id = id
        self.name = name
        self.age = age
        self.priority = priority

cur.execute("SELECT * FROM Patients")
patients = [Patient(*row) for row in cur.fetchall()]

pq = []

for p in patients:
    heapq.heappush(pq, (p.priority, p.id, p))

print("Patients in Priority Order")

while pq:
    priority, pid, patient = heapq.heappop(pq)
    print(patient.id, patient.name, patient.age, patient.priority)
    cur.execute("DELETE FROM Patients WHERE id=?", (patient.id,))
    conn.commit()

print("\nRemaining Patients")

cur.execute("SELECT * FROM Patients")
rows = cur.fetchall()

if rows:
    for row in rows:
        print(row)
else:
    print("No Patients Remaining")

conn.close()