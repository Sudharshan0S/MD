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

print(results)
