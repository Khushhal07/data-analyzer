import streamlit as st
import pandas as pd
import numpy as np
from modules.data_loader import load_data, auto_clean_data, convert_df_to_csv
from modules.analyzer import get_dataset_summary
from modules.visualizer import create_chart
from modules.chatbot import ask_dataset

st.set_page_config(page_title="AI Data Copilot", page_icon="📊", layout="wide")

# Header
st.title("📊 AI Data Analytics & Copilot Dashboard")
st.caption("Upload any dataset for instant profiling, automated cleaning, feature extraction, visualization, and AI Q&A.")

# Sidebar: Upload & Auto-Clean Controls
with st.sidebar:
    st.header("1. Upload Dataset")
    uploaded_file = st.file_uploader("Select CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    raw_df = load_data(uploaded_file)
    missing_count = int(raw_df.isnull().sum().sum())
    dup_count = int(raw_df.duplicated().sum())
    is_dirty = (missing_count > 0) or (dup_count > 0)

    # Sidebar: Smart Auto-Clean & Feature Extraction
    with st.sidebar:
        st.divider()
        st.header("2. Data Cleaning")
        if is_dirty:
            st.warning(f"Detected {missing_count:,} missing values & {dup_count:,} duplicates.")
            auto_clean = st.toggle("✨ Auto-Clean Dataset", value=True)
        else:
            st.success("✅ Dataset is already clean!")
            auto_clean = False

        df = auto_clean_data(raw_df) if auto_clean else raw_df.copy()

        st.divider()
        st.header("3. Feature Extraction")
        auto_feat = st.checkbox("⚡ Auto-Extract Features", value=False)
        if auto_feat:
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if len(num_cols) >= 2:
                new_col = f"{num_cols[0]}_to_{num_cols[1]}_ratio"
                df[new_col] = (df[num_cols[0]] / df[num_cols[1]].replace(0, np.nan)).round(2).fillna(0)
                st.info(f"Auto-created: `{new_col}`")

    # User-Guided Custom Feature Extraction (Optional)
    num_cols_all = df.select_dtypes(include=['number']).columns.tolist()
    if len(num_cols_all) >= 2:
        with st.expander("🛠️ Custom Feature Engineering (Optional - Create Your Own Feature)", expanded=False):
            fc1, fc2, fc3, fc4 = st.columns(4)
            f_col1 = fc1.selectbox("Column 1", num_cols_all, key="fc1")
            f_op = fc2.selectbox("Operation", ["Divide (/)", "Multiply (*)", "Add (+)", "Subtract (-)"])
            f_col2 = fc3.selectbox("Column 2", num_cols_all, index=1, key="fc2")
            f_name = fc4.text_input("New Feature Name", value=f"{f_col1}_custom")
            if st.checkbox("Add Custom Feature to Dataset"):
                if f_op == "Divide (/)":
                    df[f_name] = (df[f_col1] / df[f_col2].replace(0, np.nan)).round(2).fillna(0)
                elif f_op == "Multiply (*)":
                    df[f_name] = (df[f_col1] * df[f_col2]).round(2)
                elif f_op == "Add (+)":
                    df[f_name] = (df[f_col1] + df[f_col2]).round(2)
                elif f_op == "Subtract (-)":
                    df[f_name] = (df[f_col1] - df[f_col2]).round(2)
                st.success(f"Added feature `{f_name}`!")

    # TOP ROW: Live KPI Metric Cards
    overview, col_info = get_dataset_summary(df)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Rows", f"{overview['rows']:,}")
    k2.metric("Total Columns", overview["columns"])
    k3.metric("Missing Values", overview["missing_values"], delta="Cleaned" if auto_clean and missing_count > 0 else None)
    k4.metric("Duplicate Rows", overview["duplicates"], delta="Removed" if auto_clean and dup_count > 0 else None)

    st.divider()

    # MIDDLE ROW: Interactive Visualization (Left) + AI Chatbot (Right)
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.subheader("📈 Interactive Visualizer")
        cols = df.columns.tolist()
        c1, c2, c3 = st.columns(3)
        chart_type = c1.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
        x_col = c2.selectbox("X-Axis", cols, index=0)
        y_col = c3.selectbox("Y-Axis", cols, index=1 if len(cols) > 1 else 0)

        fig = create_chart(df, chart_type, x_col, y_col)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    with right_col:
        # Chatbot Header + Clear History Button
        h_col1, h_col2 = st.columns([4, 1])
        h_col1.subheader("🤖 AI Dataset Assistant")

        # Per-dataset unique history key
        history_key = f"chat_history_{uploaded_file.name}"
        if history_key not in st.session_state:
            st.session_state[history_key] = [
                {"role": "assistant", "content": f"Hello! I have loaded **{uploaded_file.name}**. Ask me anything about its rows, columns, summary, or data quality."}
            ]

        if h_col2.button("🗑️ Clear", use_container_width=True):
            st.session_state[history_key] = [
                {"role": "assistant", "content": f"Chat history cleared for **{uploaded_file.name}**. Ask a new question!"}
            ]
            st.rerun()

        # Chat Input Form
        with st.form(key="chat_form", clear_on_submit=True):
            in_col1, in_col2 = st.columns([4, 1])
            user_prompt = in_col1.text_input("Ask a question...", placeholder="e.g., tell me total rows and columns", label_visibility="collapsed")
            send_btn = in_col2.form_submit_button("Ask", use_container_width=True)

        if send_btn and user_prompt.strip():
            st.session_state[history_key].append({"role": "user", "content": user_prompt})
            reply = ask_dataset(df, user_prompt)
            st.session_state[history_key].append({"role": "assistant", "content": reply})

        chat_container = st.container(height=340)
        with chat_container:
            for msg in st.session_state[history_key]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    st.divider()

    # BOTTOM ROW: Pre-Download Data Verification (info(), isna().sum(), duplicates) & Export
    st.subheader("🔍 Pre-Download Data Health Verification & Export")
    v1, v2 = st.columns([1, 1.3])

    with v1:
        st.markdown("**Schema (`info()`) & Null Check (`isna().sum()`)**")
        health_table = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Null Count (isna)": df.isnull().sum().values,
            "Non-Null Count": df.notnull().sum().values
        })
        st.dataframe(health_table, use_container_width=True, height=240)
        st.info(f"**Duplicate Rows:** `{int(df.duplicated().sum())}` | **Final Shape:** `{df.shape[0]:,} rows × {df.shape[1]} columns`")

    with v2:
        st.markdown("**Processed Dataset Preview**")
        st.dataframe(df.head(10), use_container_width=True, height=240)
        csv_bytes = convert_df_to_csv(df)
        st.download_button(
            label="⬇️ Verified & All Good — Download Clean CSV",
            data=csv_bytes,
            file_name=f"cleaned_{uploaded_file.name.split('.')[0]}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

else:
    st.info("👈 Upload a CSV or Excel dataset from the left sidebar to launch the interactive dashboard.")
