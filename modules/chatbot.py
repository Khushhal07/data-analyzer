import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def ask_dataset(df, user_question):
    """Ultra-fast, zero-latency analytical AI assistant."""
    q = user_question.lower()

    # 1. Rows & Columns count
    if "row" in q or "colum" in q or "shape" in q or "size" in q or "record" in q:
        cols = ", ".join(df.columns.tolist())
        return (
            f"📊 **Dataset Dimensions:**\n"
            f"- **Total Rows:** `{df.shape[0]:,}`\n"
            f"- **Total Columns:** `{df.shape[1]}`\n\n"
            f"**Schema Attributes:** `{cols}`"
        )

    # 2. Topic / Overview / About
    elif "topic" in q or "about" in q or "what is" in q or "overview" in q or "explain" in q:
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        return (
            f"🤖 **Automated Schema & Domain Analysis:**\n\n"
            f"This dataset contains **{df.shape[0]:,} records** and **{df.shape[1]} features**. "
            f"It includes **{len(num_cols)} numerical metrics** (`{', '.join(num_cols[:5])}`) and "
            f"**{len(cat_cols)} categorical attributes** (`{', '.join(cat_cols[:5])}`).\n\n"
            f"Here is a quick snapshot of the records:\n\n{df.head(3).to_markdown()}"
        )

    # 3. Missing Values & Data Health
    elif "missing" in q or "null" in q or "clean" in q or "quality" in q or "health" in q:
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        dups = df.duplicated().sum()
        if missing.empty and dups == 0:
            return "✅ **Data Health Check:** The dataset is 100% clean with **0 missing values** and **0 duplicate rows**."
        return (
            f"⚠️ **Data Quality Report:**\n"
            f"- **Duplicate Rows:** `{dups}`\n"
            f"- **Missing Values Breakdown:**\n\n{missing.to_markdown()}"
        )

    # 4. Statistical Summary / Mean / Max / Min
    elif "summary" in q or "stat" in q or "mean" in q or "average" in q or "describe" in q or "max" in q or "min" in q:
        return f"📈 **Statistical Profiling & Summary Metrics:**\n\n{df.describe().round(2).to_markdown()}"

    # 5. Top / Sample rows
    elif "top" in q or "head" in q or "sample" in q or "show" in q or "preview" in q:
        return f"📄 **Top 5 Sample Records:**\n\n{df.head(5).to_markdown()}"

    # Default smart guidance
    else:
        return (
            "I have indexed all **{:,} rows** and **{} columns** of your dataset. Ask me anything like:\n"
            "- *Tell me total rows and columns*\n"
            "- *What is this dataset about?*\n"
            "- *Check data quality and missing values*\n"
            "- *Show statistical summary and averages*"
        ).format(df.shape[0], df.shape[1])
