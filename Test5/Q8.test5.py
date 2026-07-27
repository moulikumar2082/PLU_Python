import sqlite3
from collections import deque

con=sqlite3.connect("ride.db")
cur=con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Driver(ID INT,Name TEXT,Loc TEXT,Avail INT)")
cur.execute("CREATE TABLE IF NOT EXISTS Booking(CID INT,DID INT)")

cur.execute("DELETE FROM Driver")

cur.executemany("INSERT INTO Driver VALUES(?,?,?,?)",[
(1,"Raj","A",1),(2,"Amit","B",1),(3,"Neha","C",0)
])

graph={"A":["B"],"B":["A","C"],"C":["B"]}

def bfs(start):
    q=deque([start])
    seen=set()
    while q:
        x=q.popleft()
        if x not in seen:
            seen.add(x)
            cur.execute("SELECT * FROM Driver WHERE Loc=? AND Avail=1",(x,))
            d=cur.fetchone()
            if d:return d
            q+=graph[x]

d=bfs("A")
print("Driver:",d)

if d:
    cur.execute("INSERT INTO Booking VALUES(?,?)",(101,d[0]))
    cur.execute("UPDATE Driver SET Avail=0 WHERE ID=?",(d[0],))

cur.execute("""
SELECT Name,CID FROM Driver 
JOIN Booking ON Driver.ID=Booking.DID
""")

print(cur.fetchall())

con.commit()
con.close()

