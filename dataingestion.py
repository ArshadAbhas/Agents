import numpy as np
import pandas as pd

class Cleaner:
    table_count = 0
    def __init__(self, df):
        self.df = df
        Cleaner.table_count += 1
        self._table_id = Cleaner.table_count 
    def extract_ds(self):
        metadata = {}
        metadata['schema'] = self.df.columns.tolist()
        metadata['Data Types'] = str(self.df.dtypes)
        metadata['Sample Data'] = self.df.head().to_dict(orient='records')
        return metadata

    def data_issues(self):
        issues = {}
        issues['Missing Values'] = self.df.isnull().sum().to_dict()
        issues['Duplicate Rows'] = self.df.duplicated().sum()
        issues['Inconsistent Data Types'] = {col: str(dtype) for col, dtype in self.df.dtypes.items() if dtype == 'object' and any(isinstance(i, (int, float)) for i in self.df[col].dropna())}
        issues['Outliers'] = {col: self.df[col][(np.abs(self.df[col]-self.df[col].mean()) > (3*self.df[col].std()))].tolist() for col in self.df.select_dtypes(include=[np.number]).columns}
        return issues

    def summarize_issues(self):
        d = self.data_issues()
        key_p = {"Missing_Values": [], "Duplicate_Rows": [], "Wrong_dtypes": [], "Outliers": []}
        for issue, detail in d.items():
            if issue == "Missing Values":
                for col, missing_count in detail.items():
                    if missing_count > 0:
                        key_p["Missing_Values"].append(f"{col} ({missing_count})")
            elif issue == "Duplicate Rows":
                if detail > 0:
                    key_p["Duplicate_Rows"].append(f"{detail} rows")
            elif issue == "Inconsistent Data Types":
                if detail:
                    for col, dtype in detail.items():
                        key_p["Wrong_dtypes"].append(f"{col} -> {dtype}")
            elif issue == "Outliers":
                for col, outlier_list in detail.items():
                    if outlier_list:
                        key_p["Outliers"].append(col)
        return {k: v for k, v in key_p.items() if v}
    def remove_dup_missingvalues(self):
        self.df = self.df.drop_duplicates()
        self.df = self.df.fillna(pd.NA)
        return self.df
    def table_name(self):
        return f"table_{self._table_id}"