import duckdb

def drop_all_tables(db_path="expenses.duckdb"):
    # Connect to DuckDB
    con = duckdb.connect(db_path)

    # Get all table names
    tables = con.execute("SHOW TABLES").fetchall()

    if not tables:
        print("No tables found in the database.")
    else:
        for t in tables:
            table_name = t[0]
            con.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Dropped table: {table_name}")

    con.close()
    print("All tables dropped successfully.")

if __name__ == "__main__":
    drop_all_tables("expenses.duckdb")
