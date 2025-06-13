import streamlit as st
import pandas as pd

# 🔐 Password Configuration
PASSWORD = "letmein123"  # 👈 Change this to your secret password

# 🔒 Password Input
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    password = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Login successful!")
        else:
            st.error("❌ Incorrect password.")
    st.stop()

# 🟢 Main App Code Starts Here (only accessible after login)
st.set_page_config(page_title="Excel Number Search Tool", layout="centered")
st.title("📄 Excel & CSV Number Search Tool")

uploaded_file = st.file_uploader("📤 Upload Excel or CSV File", type=["xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # ✅ Limit rows to 50,000
        df = df.head(50000)

        st.success(f"✅ File uploaded! Loaded {len(df)} rows.")

        # 📅 Select Date (assume date is in first column)
        date_input = st.date_input("Select Date")

        # 🔢 Multiple Numbers Input (space-separated)
        number_input = st.text_area(
            "Enter one or more numbers (space-separated)", placeholder="1234567890 9876543210"
        )

        if st.button("🔍 Search"):
            # Convert date column to datetime.date
            df["Date"] = pd.to_datetime(df.iloc[:, 0], errors="coerce").dt.date

            # Parse space-separated numbers
            number_list = [num.strip() for num in number_input.split() if num.strip()]

            # Filter
            results = df[(df["Date"] == date_input) & (df.iloc[:, 1].astype(str).isin(number_list))]

            if not results.empty:
                st.success(f"✅ Found {len(results)} match(es).")
                st.dataframe(results)

                # 📊 Show summary of unique file names from 3rd column
                try:
                    list_file_column = results.columns[2]
                    file_summary = results[list_file_column].value_counts().reset_index()
                    file_summary.columns = ['File Name', 'Count']
                    st.markdown("### 📊 File Summary")
                    st.dataframe(file_summary)
                except Exception as e:
                    st.warning(f"⚠️ Couldn't summarize files: {e}")
            else:
                st.error("❌ No result found.")
    except Exception as e:
        st.error(f"🚫 Error reading file: {e}")
else:
    st.info("👆 Please upload a file to get started.")
