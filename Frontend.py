import streamlit as st
import pandas as pd

def is_leap(year: int) -> bool:
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False

st.title("Leap Year Dataset – Front End Design")

# File uploader for leap_years.csv
uploaded_file = st.file_uploader("Upload Leap Year CSV file", type=["csv"])

# If no file is uploaded, create a simple sample dataset
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using sample dataset from 1900 to 2050.")
    years = list(range(1900, 2051))
    df = pd.DataFrame({
        "Year": years,
        "Is_Leap_Year": [is_leap(y) for y in years]
    })

st.subheader("Original Data (First 10 Rows)")
st.write(df.head(10))

# Ensure Is_Leap_Year is boolean
if df["Is_Leap_Year"].dtype != bool:
    df["Is_Leap_Year"] = df["Is_Leap_Year"].astype(str).str.lower().isin(["true", "1", "yes"])

st.subheader("Filter Options")

filter_type = st.radio(
    "Select Filter Type:",
    ["All Years", "Only Leap Years", "Only Non-Leap Years", "Years Greater Than..."]
)

filtered_df = df.copy()

if filter_type == "Only Leap Years":
    filtered_df = df[df["Is_Leap_Year"] == True]

elif filter_type == "Only Non-Leap Years":
    filtered_df = df[df["Is_Leap_Year"] == False]

elif filter_type == "Years Greater Than...":
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())
    year_limit = st.slider("Select minimum year:", min_year, max_year, min_year)
    filtered_df = df[df["Year"] > year_limit]

st.subheader("Filtered Result")
st.write(filtered_df)
