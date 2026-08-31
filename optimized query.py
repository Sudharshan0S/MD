import time
import mysql.connector


db_connection = mysql.connector.connect(
    host="localhost",
   
    user="root",
    password="admin@123",
    database="college"
)

cursor = db_connection.cursor()
print("Successfully connected to MySQL database!")

create_table_sql = """
CREATE TABLE IF NOT EXISTS faculty (
    fid INT PRIMARY KEY,
    fname VARCHAR(255)
)
"""
cursor.execute(create_table_sql)
print("Table 'faculty' checked/created successfully!")
# -------------------------------------------------------

cursor.execute("TRUNCATE TABLE faculty")
print("Old records deleted. Starting fresh!")

sql = "INSERT INTO faculty (fid, fname) VALUES (%s, %s)"
data = []

for i in range(1, 501):
    data.append((i, f"Faculty{i}"))


sql = "INSERT INTO faculty (fid, fname) VALUES (%s, %s)"
data = []

for i in range(1, 501):
    data.append((i, f"Faculty{i}"))

cursor.executemany(sql, data)
db_connection.commit()
print("500 rows inserted successfully!")

cursor.execute("SELECT * FROM faculty")
results = cursor.fetchall()

print("\n--- Current Employees ---")
for row in results:
    print(f"ID: {row[0]} | Name: {row[1]}")

print("Optimization Technique Started")



index_stmt = "CREATE INDEX idx_fname ON faculty(fname)"
cursor.execute(index_stmt)
db_connection.commit()

print("Indexes created.")

start = 0.0
end = 0.0

# Excution of query with and without index

# With index
query = "SELECT * FROM faculty WHERE fname = 'Faculty390'"

start = time.perf_counter()
cursor.execute(query)
rows = cursor.fetchall()
end = time.perf_counter()

print(f"Execution Time WITH index : {(end - start)*1000:.4f} ms")

start = 0.0
end = 0.0

# Remove index if it exists
print("Dropping the Index")

delindex_stm = "DROP INDEX idx_fname ON faculty"
cursor.execute(delindex_stm)
db_connection.commit()

print("Index dropped")

query = "SELECT * FROM faculty WHERE fname = 'Faculty390'"

# Without Index
start = time.perf_counter()
cursor.execute(query)
cursor.fetchall()
end = time.perf_counter()

without_index = (end - start) * 1000

print(f"\nExecution Time WITHOUT Index : {without_index:.4f} ms")































"""

import duckdb
import pandas as pd
import numpy as np
import time

# create in-memory database
con = duckdb.connect()

# Reading data using pandas
dataframe = pd.read_csv("sampledata.csv")

# Reading data using duckdb
cur_time = 0
cur_time = time.time()

df = con.execute(
    " select * from read_csv_auto('sampledata.csv') Limit 5"
).df()

print(f"time : {(time.time() - cur_time)}")
print(df)

# perform analytical operation on CSV using duckdb
query = "SELECT AVG(score),COUNT(*),max(score), min(score) FROM read_csv_auto('sampledata.csv')"

cur_time = time.time()

df = con.execute(query).fetch_df()

print(
    f"time to perform analytical operations using Duckdb is : {(time.time() - cur_time)}"
)

print(df)

# perform analytical operation on CSV using dataframe.
results = []

start = time.time()

count = dataframe["Score"].count()
results.append(["COUNT", count])

average = dataframe["Score"].mean()
total = dataframe["Score"].sum()
minimum = dataframe["Score"].min()
maximum = dataframe["Score"].max()

print(
    f"time to perform analytical operations using dataframe is : {(time.time() - cur_time)}"
)

results.append(["AVERAGE", average])
results.append(["SUM", total])
results.append(["MIN", minimum])
results.append(["MAX", maximum])

print(results)"""
