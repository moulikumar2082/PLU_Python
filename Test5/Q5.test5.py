import sqlite3

conn = sqlite3.connect("cinema.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Film(
MovieID INTEGER PRIMARY KEY,
MovieName TEXT,
Category TEXT,
Rating REAL,
Views INTEGER)
""")

cursor.execute("DELETE FROM Film")

records = [
(201,"Pushpa","Action",8.7,650),
(202,"RRR","Action",9.1,850),
(203,"Interstellar","Sci-Fi",9.3,950),
(204,"Moana","Animation",8.4,550),
(205,"The Notebook","Romance",8.9,720)
]

cursor.executemany("INSERT INTO Film VALUES(?,?,?,?,?)",records)
conn.commit()

cursor.execute("SELECT * FROM Film")
films = cursor.fetchall()

print("Movie List")
for i in films:
    print(i)

films.sort(key=lambda x:x[3],reverse=True)

print("\nMovies by Rating")
for i in films:
    print(i)

movieid = int(input("\nEnter Movie ID: "))
flag = False

for i in films:
    if i[0] == movieid:
        print("\nMovie Details")
        print(i)
        flag = True
        break

if not flag:
    print("Movie Not Available")

print("\nTop Rated Movies")
for i in films[:10]:
    print(i)

print("\nHighest Viewed Movie in Each Category")

cursor.execute("""
SELECT Category, MovieName, MAX(Views)
FROM Film
GROUP BY Category
""")

for row in cursor.fetchall():
    print(row)

conn.close()