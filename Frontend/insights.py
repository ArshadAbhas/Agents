import pandas as pd

def generate_insight_prompt(csv_path):
    df = pd.read_csv(csv_path)

    basic_info = f"Columns: {', '.join(df.columns)}\n\n"
    dtypes = df.dtypes.to_string()
    description = df.describe(include='all').to_string()
    nulls = df.isnull().sum().to_string()
    unique_vals = df.nunique().to_string()
    correlation = df.corr(numeric_only=True).to_string()
    sample_data = df.head(10).to_markdown(index=False)

    predata_insights = f"""
Here is a dataset. Please analyze and provide useful insights, patterns, and recommendations.
###  Basic Info
{basic_info}
### Column Data Types
{dtypes}
### Descriptive Statistics
{description}
### Null Values Per Column
{nulls}
### Unique Values Per Column
{unique_vals}
### orrelation Matrix
{correlation}
### Sample Data (First 10 Rows)
{sample_data}
"""
    return predata_insights
