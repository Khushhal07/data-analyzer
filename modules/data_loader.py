import pandas as pd

def load_data(uploaded_file):
    """Loads CSV or Excel into a Pandas DataFrame."""
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    return None

def auto_clean_data(df):
    """Automatically removes duplicates and imputes missing values."""
    cleaned_df = df.copy()
    cleaned_df = cleaned_df.drop_duplicates()
    
    for col in cleaned_df.columns:
        if pd.api.types.is_numeric_dtype(cleaned_df[col]):
            cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
        else:
            mode_val = cleaned_df[col].mode()
            fill_val = mode_val[0] if not mode_val.empty else "Unknown"
            cleaned_df[col] = cleaned_df[col].fillna(fill_val)
            
    return cleaned_df

def convert_df_to_csv(df):
    """Converts DataFrame to UTF-8 CSV bytes for download."""
    return df.to_csv(index=False).encode('utf-8')
