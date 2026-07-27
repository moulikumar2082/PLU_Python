import sqlite3
import heapq

conn = sqlite3.connect("college.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Students(
roll INTEGER PRIMARY KEY,
name TEXT,
cgpa REAL,
skills TEXT,
status TEXT
)
""")

cur.execute("DELETE FROM Students")

data = [
    (101,"Rahul",8.5,"Python","Not Placed"),
    (102,"Priya",7.2,"Java","Not Placed"),
    (103,"Arjun",9.1,"Python,SQL","Not Placed"),
    (104,"Sneha",6.8,"C++","Not Placed"),
    (105,"Kiran",7.9,"Java,Python","Not Placed")
]

cur.executemany("INSERT INTO Students VALUES(?,?,?,?,?)", data)
conn.commit()

class Student:
    def __init__(self,roll,name,cgpa,skills,status):
        self.roll = roll
        self.name = name
        self.cgpa = cgpa
        self.skills = skills
        self.status = status

cur.execute("SELECT * FROM Students")
students = [Student(*row) for row in cur.fetchall()]

def heap_sort(arr):
    heap = []
    for s in arr:
        heapq.heappush(heap, (s.cgpa, s))
    result = []
    while heap:
        result.append(heapq.heappop(heap)[1])
    return result

def binary_search(arr,key):
    arr = sorted(arr, key=lambda x: x.roll)
    l, r = 0, len(arr)-1
    while l <= r:
        m = (l+r)//2
        if arr[m].roll == key:
            return arr[m]
        elif arr[m].roll < key:
            l = m+1
        else:
            r = m-1
    return None

print("All Students")
for s in students:
    print(s.roll, s.name, s.cgpa, s.skills, s.status)

print("\nStudents Sorted by CGPA")
sorted_students = heap_sort(students)
for s in sorted_students:
    print(s.roll, s.name, s.cgpa)

roll = int(input("\nEnter Roll Number: "))
s = binary_search(students, roll)

if s:
    print("Found:", s.roll, s.name, s.cgpa, s.skills, s.status)
else:
    print("Student Not Found")

print("\nEligible Students")
for s in students:
    if s.cgpa > 7.5:
        print(s.roll, s.name, s.cgpa)

roll = int(input("\nEnter Selected Student Roll Number: "))
cur.execute("UPDATE Students SET status='Placed' WHERE roll=?", (roll,))
conn.commit()

print("\nUpdated Student Records")
cur.execute("SELECT * FROM Students")
for row in cur.fetchall():
    print(row)

conn.close()

