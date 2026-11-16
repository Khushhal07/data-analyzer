# 📊 AI Data Analytics & Copilot Dashboard

An end-to-end, modular **AI Data Copilot** built with Python and Streamlit that automates Exploratory Data Analysis (EDA), data cleaning, feature engineering, interactive visualizations, and natural-language dataset Q&A.

## 🚀 Key Features
- **Instant Dataset Profiling:** Automatically computes dataset dimensions, missing values (`isna().sum()`), duplicate records, and statistical summaries.
- **Smart Auto-Cleaning & Pre-Download Verification:** Detects dirty data, imputes missing values (median/mode), removes duplicates, and provides a schema health check before exporting clean CSV files.
- **Auto & Custom Feature Engineering:** Generates automated numerical ratios and allows user-guided custom feature creation.
- **Interactive Visualizations:** Dynamic Bar, Line, and Scatter plots powered by Plotly.
- **Zero-Latency AI Dataset Assistant:** Per-dataset isolated chat memory allowing users to query schema details, data quality, and statistical metrics.
- **Docker Ready:** Includes `Dockerfile` and `.dockerignore` for containerized deployment.

## 🏗️ Project Architecture
```text
data-analyzer/
├── app.py                  # Main Streamlit dashboard entry point
├── modules/
│   ├── data_loader.py      # Ingestion, auto-cleaning & CSV export
│   ├── analyzer.py         # Schema profiling & summary statistics
│   ├── visualizer.py       # Interactive Plotly chart builder
│   └── chatbot.py          # Analytical Q&A assistant
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
└── README.md
```

## 🛠️ Local Setup & Run
```bash
[git clone https://github.com](https://github.com/Khushhal07/data-analyzer.git)
cd data-analyzer
pip install -r requirements.txt
streamlit run app.py
```

## 🐳 Docker Setup
```bash
docker build -t ai-data-copilot .
docker run -p 8501:8501 ai-data-copilot
```
