
import streamlit as st
import pandas as pd

st.set_page_config(page_title="📄 Smart Number Search Tool", layout="centered")
st.title("📄 Excel & CSV Smart Number Search Tool")

uploaded_file = st.file_uploader("📤 Upload Excel or CSV File", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # ✅ Load file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df = df.head(50000)
        st.success(f"✅ File uploaded! Loaded {len(df)} rows.")

        # ✅ Lowercase all headers for easier matching
        df.columns = [str(col).strip().lower() for col in df.columns]

        # ✅ Detect important columns
        date_col = next((col for col in df.columns if "date" in col), None)
        number_col = next((col for col in df.columns if "number" in col or "phone" in col), None)

        if not date_col or not number_col:
            st.error("❌ Couldn't detect 'Date' or 'Number/Phone' column. Please check headers.")
        else:
            df[date_col] = pd.to_datetime(df[date_col], format="%d/%m/%Y", errors="coerce").dt.date

            # 📅 Date range
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("From Date")
            with col2:
                end_date = st.date_input("To Date")

            # 🔢 Number input
            number_input = st.text_area(
                "Enter one or more numbers (space-separated)",
                placeholder="1234567890 9876543210"
            )

            if st.button("🔍 Search"):
                number_list = [num.strip() for num in number_input.split() if num.strip()]

                # ✅ Filter by date & number
                filtered_df = df[
                    (df[date_col] >= start_date) &
                    (df[date_col] <= end_date) &
                    (df[number_col].astype(str).isin(number_list))
                ]

                if not filtered_df.empty:
                    st.success(f"✅ Found {len(filtered_df)} match(es).")

                    st.dataframe(filtered_df)

                    # 📁 List file column = 3rd column (index 2)
                    if len(df.columns) >= 3:
                        list_file_col = df.columns[2]
                        file_counts = (
                            filtered_df[list_file_col]
                            .value_counts()
                            .reset_index()
                            .rename(columns={"index": "List File", list_file_col: "Count"})
                        )

                        st.subheader("📁 List File Summary")
                        st.dataframe(file_counts)
                else:
                    st.error("❌ No result found.")

    except Exception as e:
        st.error(f"🚫 Error reading file: {e}")
else:
    st.info("👆 Please upload a file to get started.")
