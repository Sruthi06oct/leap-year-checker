# 🌙 Leap Year Checker – Data Analysis & Streamlit Web App

A complete data analysis project built using **Python, Pandas, NumPy, Matplotlib, and Streamlit**, focusing on understanding leap years, performing data wrangling, generating visualizations, and building an interactive web application.

This project is designed as an end-to-end **case study** covering all major data science tasks:
✔ Data Loading  
✔ Data Cleaning  
✔ Data Wrangling  
✔ Filtering & Indexing  
✔ Aggregation & Grouping  
✔ Visualization  
✔ Streamlit App Development  

---

## 📌 **Project Overview**

A leap year occurs every 4 years, except century years unless divisible by 400.  
This project uses a dataset containing years from **1900–2050**, along with their leap-year status, leap rules, and derived fields.

We analyzed the dataset, generated insights, and created an interactive app to explore leap year logic easily.

---

## 🗂 **Features**

### 🔹 1. Data Loading & Inspection
- Load dataset using Pandas  
- Display first and last rows  
- Summary statistics & info  
- Missing value detection  

### 🔹 2. Data Cleaning
- Remove duplicate rows  
- Handle missing values  
- Fix datatype inconsistencies  

### 🔹 3. Data Wrangling
- Add:
  - `Leap_Code` (1/0)
  - `Leap_Reason` (text explanation)
  - `Year_Normalized` (0–1 scaled value)
- Convert columns into usable formats  

### 🔹 4. Filtering & Indexing
- View only leap years  
- View only non-leap years  
- Filter years greater than mean  
- Use `loc` and `iloc` indexing  

### 🔹 5. Aggregation & Grouping
- Group by leap reason  
- Group by year ranges  
- Calculate:
  - Total leap years  
  - Leap ratios  
  - Summary metrics  

### 🔹 6. Visualization (Matplotlib)
- Line Plot  
- Bar Chart  
- Histogram  
- Scatter Plot  

### 🔹 7. Streamlit Web App
Interactive features:
- Upload your own CSV file  
- Preview dataset  
- Explore filtered results  
- Visualize leap year trends  
- Check leap year for any input year  

---

## 🧠 **Leap Year Rules Used**

```txt
If year % 400 == 0 → Leap Year  
Else if year % 100 == 0 → Not a Leap Year  
Else if year % 4 == 0 → Leap Year  
Else → Not a Leap Year  
