import streamlit as st
import pandas as pd
from datetime import timedelta
from collections import Counter

st.set_page_config(page_title="Excel & CSV Number Search Tool", layout="centered")
st.title("📄 Excel & CSV Number Search Tool")

uploaded_file = st.file_uploader("📤 Upload Excel or CSV File", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df = df.head(50000)
        df["Date"] = pd.to_datetime(df.iloc[:, 0], errors="coerce").dt.date
        st.success(f"✅ File uploaded! Loaded {len(df)} rows.")

        # 📅 Single date range
        st.subheader("📅 Select Date Range")
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date")
        with col2:
            to_date = st.date_input("To Date")

        if from_date > to_date:
            st.warning("⚠️ 'From Date' cannot be after 'To Date'.")
        else:
            date_range = pd.date_range(start=from_date, end=to_date).date

            # 🔢 Multiple Numbers Input
            number_input = st.text_area(
                "Enter one or more numbers (space-separated)",
                placeholder="1234567890 9876543210"
            )

            if st.button("🔍 Search"):
                number_list = [num.strip() for num in number_input.split() if num.strip()]
                results = df[df["Date"].isin(date_range) & df.iloc[:, 1].astype(str).isin(number_list)]

                if not results.empty:
                    st.success(f"✅ Found {len(results)} match(es).")
                    st.dataframe(results)

                    # 📁 Count list file (3rd column)
                    list_counts = Counter(results.iloc[:, 2])
                    count_df = pd.DataFrame(list_counts.items(), columns=["List File", "Count"])
                    st.subheader("📁 List File Frequency")
                    st.dataframe(count_df)
                else:
                    st.error("❌ No result found.")

    except Exception as e:
        st.error(f"🚫 Error reading file: {e}")
else:
    st.info("👆 Please upload a file to get started.")
