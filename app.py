import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel & CSV Number Search Tool", layout="centered")
st.title("📄 Excel & CSV Number Search Tool")

uploaded_file = st.file_uploader("📤 Upload Excel or CSV File", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # 📄 Load Excel or CSV
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # ✅ Limit to first 50,000 rows
        df = df.head(50000)

        st.success(f"✅ File uploaded! Loaded {len(df)} rows.")

        # ✅ Parse date using dd/mm/yyyy format
        df["Date"] = pd.to_datetime(df.iloc[:, 0], format="%d/%m/%Y", errors="coerce").dt.date

        # 📅 Select date range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From Date")
        with col2:
            end_date = st.date_input("To Date")

        # 🔢 Input numbers
        number_input = st.text_area(
            "Enter one or more numbers (space-separated)",
            placeholder="1234567890 9876543210"
        )

        if st.button("🔍 Search"):
            # Clean number input
            number_list = [num.strip() for num in number_input.split() if num.strip()]

            # ✅ Filter by date range and number match
            filtered_df = df[
                (df["Date"] >= start_date) &
                (df["Date"] <= end_date) &
                (df.iloc[:, 1].astype(str).isin(number_list))
            ]

            if not filtered_df.empty:
                st.success(f"✅ Found {len(filtered_df)} match(es).")
                st.dataframe(filtered_df)

                # 📊 Show unique List File counts
                file_counts = (
                    filtered_df.iloc[:, 2]
                    .value_counts()
                    .reset_index()
                    .rename(columns={"index": "List File", filtered_df.columns[2]: "Count"})
                )

                st.subheader("📁 List File Summary")
                st.dataframe(file_counts)

            else:
                st.error("❌ No result found.")

    except Exception as e:
        st.error(f"🚫 Error reading file: {e}")
else:
    st.info("👆 Please upload a file to get started.")
