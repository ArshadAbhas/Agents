import pandas as pd 
import duckdb
from  dataingestion import Cleaner

class NewTable:
   def __init__(self, file):
      self.df =  pd.read_excel(file)
  

   def addtable(self):
      cleaner = Cleaner(self.df)
      con = duckdb.connect(database='my_database.db', read_only=False)
      cleaned_df = cleaner.remove_dup_missingvalues()
      con.register("cleaned_df_view", cleaned_df)
      table_name = cleaner.table_name()
      con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM cleaned_df_view")
      con.close()
      return table_name 
   
