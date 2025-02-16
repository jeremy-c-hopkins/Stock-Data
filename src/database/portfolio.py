import sqlite3

con = sqlite3.connect("/home/bread/Coding/Finance/src/database/portfolio.db")

cur = con.cursor()

sql_query = """SELECT name FROM sqlite_master  
  WHERE type='table';"""

cur.execute(sql_query)

print(cur.fetchall())

