import sqlite3

conn = sqlite3.connect("bank.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Transactions(
id INTEGER PRIMARY KEY,
account_no TEXT,
amount REAL,
date TEXT,
type TEXT
)
""")

cur.execute("DELETE FROM Transactions")

data = [
    (101,"ACC1001",5000,"2026-07-01","Credit"),
    (102,"ACC1002",2000,"2026-07-02","Debit"),
    (103,"ACC1003",12000,"2026-07-03","Credit"),
    (104,"ACC1001",1500,"2026-07-04","Debit"),
    (105,"ACC1004",8000,"2026-07-05","Credit"),
    (106,"ACC1002",3000,"2026-07-06","Debit"),
    (107,"ACC1005",25000,"2026-07-07","Credit")
]

cur.executemany("INSERT INTO Transactions VALUES(?,?,?,?,?)", data)
conn.commit()

class Transaction:
    def __init__(self,id,account_no,amount,date,type):
        self.id = id
        self.account_no = account_no
        self.amount = amount
        self.date = date
        self.type = type

cur.execute("SELECT * FROM Transactions")
transactions = [Transaction(*row) for row in cur.fetchall()]

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2].amount
    left = [x for x in arr if x.amount < pivot]
    middle = [x for x in arr if x.amount == pivot]
    right = [x for x in arr if x.amount > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def binary_search(arr,key):
    arr = sorted(arr,key=lambda x:x.id)
    l,r = 0,len(arr)-1
    while l<=r:
        m = (l+r)//2
        if arr[m].id == key:
            return arr[m]
        elif arr[m].id < key:
            l = m+1
        else:
            r = m-1
    return None

print("All Transactions")
for t in transactions:
    print(t.id,t.account_no,t.amount,t.date,t.type)

print("\nSorted by Amount")
sorted_transactions = quick_sort(transactions)
for t in sorted_transactions:
    print(t.id,t.amount)

tid = int(input("\nEnter Transaction ID: "))
t = binary_search(transactions,tid)

if t:
    print("Found:",t.id,t.account_no,t.amount,t.date,t.type)
else:
    print("Transaction Not Found")

credit = 0
debit = 0

for t in transactions:
    if t.type == "Credit":
        credit += t.amount
    else:
        debit += t.amount

print("\nTotal Credit:",credit)
print("Total Debit:",debit)

print("\nTop 5 Highest Transactions")
top = sorted(transactions,key=lambda x:x.amount,reverse=True)[:5]

for t in top:
    print(t.id,t.account_no,t.amount)

conn.close()