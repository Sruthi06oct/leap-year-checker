import streamlit as st
import pandas as pd

# Helper function
def leap_reason(year):
    if year % 400 == 0:
        return "Divisible by 400"
    elif year % 100 == 0:
        return "Divisible by 100 but not 400"
    elif year % 4 == 0:
        return "Divisible by 4 but not 100"
    else:
        return "Not divisible by 4"

st.title("Leap Year Dataset – Grouping Analysis")

uploaded_file = st.file_uploader("Upload Leap Year CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using sample dataset for grouping example.")
    years = list(range(1900, 2051))
    df = pd.DataFrame({
        "Year": years,
        "Is_Leap_Year": [year % 400 == 0 or (year % 4 == 0 and year % 100 != 0) for year in years]
    })

# Create derived columns
df["Leap_Code"] = df["Is_Leap_Year"].astype(int)
df["Leap_Reason"] = df["Year"].apply(leap_reason)

# Create year group ranges
df["Year_Group"] = pd.cut(
    df["Year"],
    bins=[0, 1949, 1999, 2100],
    labels=["Before 1950", "1950–1999", "2000 and later"],
    include_lowest=True
)

st.subheader("Select Grouping Column")
group_col = st.selectbox("Choose a column to group by:", ["Leap_Reason", "Year_Group"])

st.subheader(f"Grouping by {group_col}")

grouped_data = df.groupby(group_col)["Leap_Code"].agg(["count", "sum", "mean"]).reset_index()

grouped_data = grouped_data.rename(columns={
    "count": "Total Years",
    "sum": "Total Leap Years",
    "mean": "Leap Year Ratio"
})

st.table(grouped_data)
