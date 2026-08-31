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
