import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🤖 AI Data Analyst")
st.write("Upload a CSV dataset and get instant insights, charts, and summary.")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# Function to generate insights
def generate_insights(df):

    insights = []

    rows, cols = df.shape
    insights.append(f"The dataset contains {rows} rows and {cols} columns.")

    # Numeric columns
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        highest_mean = df[numeric_cols].mean().idxmax()
        insights.append(f"{highest_mean} has the highest average value.")

        highest_var = df[numeric_cols].var().idxmax()
        insights.append(f"{highest_var} shows the highest variability.")

    # Categorical dominance
    cat_cols = df.select_dtypes(include="object").columns

    for col in cat_cols[:2]:  # limit to avoid too many insights
        top = df[col].value_counts().idxmax()
        insights.append(f"{top} dominates the {col} category.")

    # Missing values
    missing = df.isnull().sum().sum()

    if missing > 0:
        insights.append(f"There are {missing} missing values in the dataset.")
    else:
        insights.append("No missing values detected.")

    return insights


if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully!")

    # Dataset Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # Dataset Summary
    st.subheader("📊 Dataset Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Shape of Dataset")
        st.write(df.shape)

        st.write("Column Names")
        st.write(df.columns.tolist())

    with col2:
        st.write("Data Types")
        st.dataframe(df.dtypes)

    st.subheader("Statistical Summary")
    st.dataframe(df.describe())

    # Missing Values
    st.subheader("⚠ Missing Values")

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        st.success("No missing values found.")
    else:
        st.dataframe(missing)

    # Automatic Charts
    st.subheader("📈 Automatic Charts")

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        for col in numeric_cols:
            fig = px.histogram(
                df,
                x=col,
                title=f"Distribution of {col}"
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No numeric columns available for visualization.")

    # Insights
    st.subheader("🧠 Data Insights")

    insights = generate_insights(df)

    for insight in insights:
        st.write("•", insight)

else:
    st.info("Please upload a CSV file to start analysis.")