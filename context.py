import pandas as pd 
import numpy as np

df = pd.read_csv(r"/home/arshad-ahmed/Documents/Agents/Sample_Data/Bakery.csv")
print(df.head())

class Context:
    id = 0
    def __init__ (self, df, rows):
        self.df = df
        self.rows = rows
        Context.id += 1
        self.metaData = {}
    def extract_num_columns(self):
        return self.df.shape[1]

    def extract_column_names(self):
        return self.df.columns.tolist()

    def extract_data_types(self):
        return self.df.dtypes.astype(str).to_dict()

    def extract_sample_row(self):
        return self.df.head(1).to_dict(orient="records")

    def extract_summary_stats(self):
        return self.df.describe(include='all').to_dict()
    def sample(self):
        return df.head(self.rows).to_markdown(index=False)

    def extract_metadata(self):
        self.metaData['Number of Columns'] = self.extract_num_columns()
        self.metaData['Schema'] = self.extract_column_names()
        self.metaData['Data Types'] = self.extract_data_types()
        self.metaData['Sample'] = self.extract_sample_row()
        self.metaData['Summary Stats'] = self.extract_summary_stats()
        return self.metaData


