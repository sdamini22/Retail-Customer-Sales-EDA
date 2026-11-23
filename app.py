import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retail Customer Sales Dashboard", page_icon="🛍️", layout="wide")

st.title("🛍️ Retail Customer Sales Dashboard")
st.caption("Explore retail sales data with interactive summaries and visualizations.")

# The repository dataset loads automatically for every visitor.
# Uploading another CSV is optional and only affects the current session.
from pathlib import Path

DEFAULT_DATASET = Path(__file__).resolve().parent / "retail_customer_sales_dataset.csv"
uploaded_file = st.sidebar.file_uploader(
    "Optional: analyse a different retail sales CSV", type=["csv"]
)

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.info("Using your uploaded CSV for this session.")
    else:
        df = pd.read_csv(DEFAULT_DATASET)
        st.sidebar.info("Showing the included retail sales dataset automatically.")
except (OSError, ValueError, pd.errors.ParserError) as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

if df.empty:
    st.warning("The uploaded CSV is empty.")
    st.stop()

# Basic data preparation for analysis only; the uploaded file is not overwritten.
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
date_cols = []
for col in df.columns:
    if df[col].dtype == "object":
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().mean() >= 0.7:
            date_cols.append(col)

missing_cells = int(df.isna().sum().sum())
duplicate_rows = int(df.duplicated().sum())

st.subheader("📌 Dataset Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Records", f"{len(df):,}")
c2.metric("Total Columns", f"{len(df.columns):,}")
c3.metric("Missing Cells", f"{missing_cells:,}")
c4.metric("Duplicate Rows", f"{duplicate_rows:,}")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Data Preview", "Data Quality", "Visual Analysis", "Download"]
)

with tab1:
    st.subheader("First rows of the dataset")
    st.dataframe(df.head(20), use_container_width=True)
    st.subheader("Column Information")
    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [str(x) for x in df.dtypes],
        "Non-Null Values": [int(df[c].notna().sum()) for c in df.columns],
        "Missing Values": [int(df[c].isna().sum()) for c in df.columns]
    })
    st.dataframe(info, use_container_width=True)

with tab2:
    st.subheader("Missing Values")
    missing = df.isna().sum().sort_values(ascending=False)
    missing = missing[missing > 0]
    if missing.empty:
        st.success("No missing values found.")
    else:
        missing_df = pd.DataFrame({
            "Missing Count": missing,
            "Missing Percentage": (missing / len(df) * 100).round(2)
        })
        st.dataframe(missing_df, use_container_width=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        missing_df["Missing Count"].plot(kind="bar", ax=ax)
        ax.set_ylabel("Number of missing values")
        ax.set_xlabel("Columns")
        ax.set_title("Missing Values by Column")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Duplicate Records")
    st.write(f"Duplicate rows detected: **{duplicate_rows}**")
    st.subheader("Statistical Summary")
    if numeric_cols:
        st.dataframe(df[numeric_cols].describe().T, use_container_width=True)
    else:
        st.info("No numeric columns available for statistical summary.")

with tab3:
    st.subheader("Explore Charts")
    if numeric_cols:
        selected_num = st.selectbox("Choose a numeric column", numeric_cols)
        fig, ax = plt.subplots(figsize=(9, 4))
        sns.histplot(df[selected_num].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {selected_num}")
        st.pyplot(fig)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 3))
        sns.boxplot(x=df[selected_num], ax=ax)
        ax.set_title(f"Outlier Overview: {selected_num}")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No numeric columns found for numeric charts.")

    if categorical_cols:
        selected_cat = st.selectbox("Choose a category column", categorical_cols)
        top_values = df[selected_cat].fillna("Missing").astype(str).value_counts().head(15)
        fig, ax = plt.subplots(figsize=(10, 4))
        top_values.sort_values().plot(kind="barh", ax=ax)
        ax.set_title(f"Top categories in {selected_cat}")
        ax.set_xlabel("Count")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("No categorical columns found for category charts.")

    if len(numeric_cols) >= 2:
        st.subheader("Correlation Heatmap")
        corr = df[numeric_cols].corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        ax.set_title("Correlation Between Numeric Columns")
        st.pyplot(fig)
        plt.close(fig)

    if date_cols:
        st.subheader("Date-wise Trend")
        date_col = st.selectbox("Choose a date column", date_cols)
        temp = df.copy()
        temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
        trend = temp.dropna(subset=[date_col]).groupby(temp[date_col].dt.date).size()
        if not trend.empty:
            st.line_chart(trend)
        else:
            st.info("No valid dates available in this column.")

with tab4:
    st.subheader("Download Dataset")
    st.download_button(
        "Download current CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="retail_customer_sales_data.csv",
        mime="text/csv"
    )
    st.caption("This dashboard does not change or overwrite your original CSV file.")

st.sidebar.success("Dataset loaded successfully!")
st.sidebar.write(f"Rows: {len(df):,} | Columns: {len(df.columns):,}")
