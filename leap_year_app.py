import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from io import StringIO

# ------------- Helper Functions -------------

def is_leap(year: int) -> bool:
    """Return True if a year is a leap year, else False."""
    if pd.isna(year):
        return False
    year = int(year)
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False


def leap_reason(year: int) -> str:
    """Return textual explanation for leap-year status."""
    if pd.isna(year):
        return "Invalid year"
    year = int(year)
    if year % 400 == 0:
        return "Divisible by 400"
    elif year % 100 == 0:
        return "Divisible by 100 but not 400"
    elif year % 4 == 0:
        return "Divisible by 4 but not 100"
    else:
        return "Not divisible by 4"


def create_sample_dataset():
    """Create a leap_years dataframe in memory."""
    years = list(range(1900, 2051))
    data = {
        "Year": years,
        "Is_Leap_Year": [is_leap(y) for y in years],
    }
    df = pd.DataFrame(data)
    return df


def ensure_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Make sure Year, Is_Leap_Year, Leap_Code, Leap_Reason, Year_Normalized exist.
    Works even if uploaded CSV does not have Is_Leap_Year column.
    """
    df = df.copy()

    # 1. Ensure a 'Year' column exists (case-insensitive support)
    if "Year" not in df.columns:
        year_like = [c for c in df.columns if "year" in c.lower()]
        if year_like:
            df = df.rename(columns={year_like[0]: "Year"})
        else:
            raise ValueError(
                "No 'Year' column found in the dataset. "
                "Please ensure your CSV has a 'Year' column."
            )

    # 2. Ensure Year is numeric
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    # 3. Ensure Is_Leap_Year exists
    if "Is_Leap_Year" not in df.columns:
        # Create it from Year using our is_leap function
        df["Is_Leap_Year"] = df["Year"].apply(is_leap)
    else:
        # Standardize to boolean: handle 0/1, "true"/"false", "yes"/"no", etc.
        if df["Is_Leap_Year"].dtype != bool:
            df["Is_Leap_Year"] = (
                df["Is_Leap_Year"]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["true", "1", "yes"])
            )

    # 4. Encoded leap code (0 / 1)
    df["Leap_Code"] = df["Is_Leap_Year"].astype(int)

    # 5. Reason column
    if "Leap_Reason" not in df.columns:
        df["Leap_Reason"] = df["Year"].apply(leap_reason)

    # 6. Normalization for Year (ignoring NaNs)
    scaler = MinMaxScaler()
    # To avoid error if all years are NaN
    if df["Year"].notna().any():
        df["Year_Normalized"] = scaler.fit_transform(df[["Year"]])
    else:
        df["Year_Normalized"] = np.nan

    return df


# ------------- Main App -------------

def main():
    st.title("Leap Year Checker – Data Analysis & Streamlit App")
    st.write(
        """
        This app demonstrates **Leap Year Checker Case Study** using:
        - Data loading & inspection  
        - Data cleaning  
        - Data wrangling  
        - Filtering & indexing  
        - Aggregation & grouping  
        - Visualization  
        in a Streamlit interface.
        """
    )

    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Go to Section:",
        [
            "1. Upload / Sample Data",
            "2. Data Loading & Inspection",
            "3. Data Cleaning",
            "4. Data Wrangling",
            "5. Filtering & Indexing",
            "6. Aggregation & Grouping",
            "7. Visualization",
            "8. Leap Year Checker (Single Year)"
        ],
    )

    # --------- Section 1: Upload or Sample Data ---------
    st.sidebar.markdown("---")
    st.sidebar.write("### Dataset Options")

    uploaded_file = st.sidebar.file_uploader("Upload leap_years.csv", type=["csv"])
    use_sample = st.sidebar.checkbox(
        "Use built-in sample dataset (1900–2050)",
        value=True if uploaded_file is None else False
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        if use_sample:
            df = create_sample_dataset()
        else:
            st.warning("Upload a CSV file or enable sample dataset.")
            return

    # Make sure core derived columns exist
    df = ensure_derived_columns(df)

    # --------- Section 1: Upload / Sample Data ---------
    if section == "1. Upload / Sample Data":
        st.header("Task 1: Data Loading and Inspection (Basic View)")
        st.write("### Preview of Dataset")
        st.write(df.head())

        st.write("### Data Types")
        st.write(df.dtypes)

        st.write("### Shape")
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # --------- Section 2: Data Loading & Inspection ---------
    elif section == "2. Data Loading & Inspection":
        st.header("Task 1: Data Loading and Inspection")

        st.subheader("1. Head (First 5 Rows)")
        st.write(df.head())

        st.subheader("2. Tail (Last 5 Rows)")
        st.write(df.tail())

        st.subheader("3. Info (Summary)")
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)

        st.subheader("4. Describe (Statistical Summary)")
        st.write(df.describe(include="all"))

        st.subheader("5. Missing Values Check")
        st.write(df.isnull().sum())
        st.write("Any missing values? ", df.isnull().values.any())
        st.write("Total missing values: ", int(df.isnull().values.sum()))

    # --------- Section 3: Data Cleaning ---------
    elif section == "3. Data Cleaning":
        st.header("Task 2: Data Cleaning")

        st.subheader("Missing Values Before Cleaning")
        st.write(df.isnull().sum())

        # Drop NaNs
        df_dropna = df.dropna()
        st.subheader("After Dropping Rows with Missing Values")
        st.write(df_dropna.isnull().sum())

        # Fill NaNs (example with 0)
        df_filled = df.fillna(0)
        st.subheader("After Filling Missing Values (with 0)")
        st.write(df_filled.isnull().sum())

        st.subheader("Removing Duplicate Rows")
        before = df.shape[0]
        df_unique = df.drop_duplicates()
        after = df_unique.shape[0]

        st.write(f"Rows before removing duplicates: {before}")
        st.write(f"Rows after removing duplicates:  {after}")
        st.write("Preview (after removing duplicates):")
        st.write(df_unique.head())

    # --------- Section 4: Data Wrangling ---------
    elif section == "4. Data Wrangling":
        st.header("Task 3: Data Wrangling")

        st.subheader("Data Types Before Conversion")
        st.write(df.dtypes)

        st.write("We ensure Year is numeric, Is_Leap_Year is boolean, and create Leap_Code & Leap_Reason.")
        st.subheader("Data After Wrangling (First 10 Rows)")
        st.write(df[["Year", "Is_Leap_Year", "Leap_Code", "Leap_Reason", "Year_Normalized"]].head(10))

        st.subheader("Apply Transformations or Encoding on String Columns")
        df_str = df.copy()
        df_str["Leap_Reason"] = df_str["Leap_Reason"].astype("string")
        df_str["Is_Leap_Year"] = df_str["Is_Leap_Year"].astype("string")
        df_str["Reason_Code"] = df_str["Leap_Reason"].astype("category").cat.codes
        df_str["Leap_Reason_Upper"] = df_str["Leap_Reason"].str.upper()

        st.write("Transformed String Columns (First 10 Rows):")
        st.write(df_str[["Year", "Is_Leap_Year", "Leap_Reason", "Reason_Code", "Leap_Reason_Upper"]].head(10))

    # --------- Section 5: Filtering & Indexing ---------
    elif section == "5. Filtering & Indexing":
        st.header("Task 4: Filtering and Indexing")

        st.subheader("Original Data (First 10 Rows)")
        st.write(df.head(10))

        st.subheader("Filter by Leap Status")
        filter_type = st.radio(
            "Filter Type:",
            ["All Years", "Only Leap Years", "Only Non-Leap Years"],
            horizontal=True
        )

        if filter_type == "Only Leap Years":
            filtered = df[df["Is_Leap_Year"] == True]
        elif filter_type == "Only Non-Leap Years":
            filtered = df[df["Is_Leap_Year"] == False]
        else:
            filtered = df

        st.write("Filtered Result:")
        st.write(filtered.head(20))

        st.subheader("Filter by Year > Mean")
        mean_year = df["Year"].mean()
        st.write(f"Mean of Year: {mean_year:.2f}")
        filtered_mean = df[df["Year"] > mean_year]
        st.write("Rows where Year > mean:")
        st.write(filtered_mean.head(20))

        st.subheader("Multiple Conditions (Leap Years after 2000)")
        filtered_multi = df[(df["Is_Leap_Year"] == True) & (df["Year"] > 2000)]
        st.write(filtered_multi.head(20))

        st.subheader("Indexing with loc and iloc")
        st.write("Label-based (loc) – rows 0–5, Year & Is_Leap_Year:")
        st.write(df.loc[0:5, ["Year", "Is_Leap_Year"]])

        st.write("Position-based (iloc) – rows 0–5, first 3 columns:")
        st.write(df.iloc[0:5, 0:3])

    # --------- Section 6: Aggregation & Grouping ---------
    elif section == "6. Aggregation & Grouping":
        st.header("Task 5: Aggregation and Grouping")

        st.subheader("Numeric Column Aggregation")
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
        st.write("Numeric Columns:", list(numeric_cols))

        aggregations = df[numeric_cols].agg(
            ["sum", "mean", "median", "min", "max", "count", "std", "var"]
        )
        st.write("Statistical Summary:")
        st.write(aggregations)

        st.subheader("Grouping by Year Range")
        df_group = df.copy()
        df_group["Year_Group"] = pd.cut(
            df_group["Year"],
            bins=[0, 1949, 1999, 2100],
            labels=["Before 1950", "1950–1999", "2000 and later"],
            include_lowest=True
        )
        df_group["Leap_Code"] = df_group["Is_Leap_Year"].astype(int)

        group_year = df_group.groupby("Year_Group", observed=True)["Leap_Code"].agg(["count", "sum", "mean"])
        group_year = group_year.rename(columns={
            "count": "Total Years",
            "sum": "Total Leap Years",
            "mean": "Leap Year Ratio"
        })

        st.write("Grouped by Year Range:")
        st.write(group_year)

        st.subheader("Grouping by Leap_Reason")
        group_reason = df.groupby("Leap_Reason", observed=True).agg({
            "Year": ["count", "min", "max"],
            "Leap_Code": ["sum", "mean"]
        })

        group_reason = group_reason.rename(columns={
            "count": "Total Years",
            "min": "Earliest Year",
            "max": "Latest Year",
            "sum": "Total Leap Years",
            "mean": "Leap Year Ratio"
        })

        st.write("Grouped by Leap Reason:")
        st.write(group_reason)

    # --------- Section 7: Visualization ---------
    elif section == "7. Visualization":
        st.header("Task 6: Visualization")

        # Line Plot
        st.subheader("Line Plot: Leap_Code over Years")
        fig1, ax1 = plt.subplots()
        ax1.plot(df["Year"], df["Leap_Code"])
        ax1.set_title("Line Plot of Leap Years Over Time")
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Leap_Code (1 = Leap, 0 = Non-Leap)")
        ax1.grid(True)
        st.pyplot(fig1)

        # Bar Chart - Leap Reason counts
        st.subheader("Bar Chart: Leap Reason Counts")
        counts = df["Leap_Reason"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.bar(counts.index, counts.values)
        ax2.set_title("Bar Chart of Leap Year Rules")
        ax2.set_xlabel("Leap Rule Category")
        ax2.set_ylabel("Count of Years")
        plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
        ax2.grid(True)
        st.pyplot(fig2)

        # Histogram
        st.subheader("Histogram: Leap vs Non-Leap Frequency")
        fig3, ax3 = plt.subplots()
        ax3.hist(df["Leap_Code"], bins=2)
        ax3.set_title("Histogram of Leap vs Non-Leap Years")
        ax3.set_xlabel("Leap_Code (0 = Non-Leap, 1 = Leap)")
        ax3.set_ylabel("Frequency")
        ax3.grid(True)
        st.pyplot(fig3)

        # Scatter Plot
        st.subheader("Scatter Plot: Year vs Leap_Code")
        fig4, ax4 = plt.subplots()
        ax4.scatter(df["Year"], df["Leap_Code"])
        ax4.set_title("Scatter Plot of Leap Years Over Time")
        ax4.set_xlabel("Year")
        ax4.set_ylabel("Leap_Code")
        ax4.grid(True)
        st.pyplot(fig4)

    # --------- Section 8: Simple Leap Year Checker ---------
    elif section == "8. Leap Year Checker (Single Year)":
        st.header("Interactive Leap Year Checker")

        year_input = st.number_input("Enter a Year:", min_value=1, max_value=9999, value=2024, step=1)
        if st.button("Check Leap Year"):
            result = is_leap(int(year_input))
            reason = leap_reason(int(year_input))
            if result:
                st.success(f"✅ {int(year_input)} is a LEAP YEAR. ({reason})")
            else:
                st.error(f"❌ {int(year_input)} is NOT a leap year. ({reason})")


if __name__ == "__main__":
    main()
