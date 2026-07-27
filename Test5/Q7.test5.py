import sqlite3
from datetime import datetime

con = sqlite3.connect("attendance.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Attendance(ID INT, Name TEXT, InTime TEXT, OutTime TEXT)")

cur.execute("DELETE FROM Attendance")

data = [
    (101,"Rahul","09:00","18:00"),
    (102,"Amit","08:30","17:30"),
    (103,"Priya","09:15","19:00"),
    (104,"Neha","10:00","18:30")
]

cur.executemany("INSERT INTO Attendance VALUES(?,?,?,?)", data)
con.commit()

def hours(a,b):
    return (datetime.strptime(b,"%H:%M")-datetime.strptime(a,"%H:%M")).seconds/3600

cur.execute("SELECT * FROM Attendance")
emp = [[x[0],x[1],hours(x[2],x[3])] for x in cur.fetchall()]

print("Records:")
for e in emp:
    print(e)

emp.sort(key=lambda x:x[2], reverse=True)

print("\nSorted:")
for e in emp:
    print(e)

emp.sort()

def search(id):
    l,h=0,len(emp)-1
    while l<=h:
        m=(l+h)//2
        if emp[m][0]==id:
            return emp[m]
        elif emp[m][0]<id:
            l=m+1
        else:
            h=m-1

print("\nSearch:", search(103))

print("\nAbove 45 Hours:")
for e in emp:
    if e[2]*5 > 45:
        print(e)

con.close()

