import duckdb
con = duckdb.connect(database='my_database.db', read_only=False)
print(con.execute("SHOW TABLES").fetchdf())
con.execute("DROP TABLE table_1")
print(con.execute("SHOW TABLES").fetchdf())
print("hi")