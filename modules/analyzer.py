import pandas as pd

def get_dataset_summary(df):
    """Dataset ka basic overview aur column-wise report banata hai."""
    overview = {
        "rows": df.shape[0],       # [0] lagane se sirf rows ka number (30) milega
        "columns": df.shape[1],    # [1] lagane se sirf columns ka number (7) milega
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }
    
    # Har column ka data type aur missing count
    col_info = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })
    
    return overview, col_info
