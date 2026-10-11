import streamlit as st
import pandas as pd
from datetime import date
import cloud_db as db

# Page Configuration
st.set_page_config(
    page_title="Agri-Dairy Enterprise Manager",
    page_icon="🌾",
    layout="wide"
)

# --- ADVANCED AGRICULTURAL & DAIRY THEME CSS ---
st.markdown("""
    <style>
    /* Main Background & Font Styling */
    .stApp {
        background: linear-gradient(to bottom right, #f4f9f4, #eaf2e8);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1b4332;
        color: white;
    }
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #1b4332;
        font-weight: 700;
    }
    
    /* Metric Cards Styling (Agriculture & Dairy Vibe) */
    .stMetric {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(27, 67, 50, 0.08);
        border-left: 5px solid #2d6a4f;
        border-top: 1px solid #e0e0e0;
    }
    .stMetric label {
        color: #40916c !important;
        font-weight: 600 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1b4332 !important;
        font-weight: 800 !important;
    }

    /* Buttons Styling */
    .stButton>button {
        background-color: #2d6a4f;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b4332;
        color: #ffffff;
        border: none;
    }
    
    /* Dataframe Container */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Main Title Header with Agri-Dairy Icon
st.title("🌾 Agri-Dairy Enterprise Manager")
st.markdown("### 🐄 ڈیری فارم اور زرعی رقبہ کا جدید ترین مینجمنٹ سسٹم")
st.markdown("---")

# Navigation Menu inside Styled Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/cow-breed.png", width=70)
    st.header("فارم کنٹرول پینل")
    menu = st.selectbox(
        "مینو منتخب کریں", 
        ["📊 ڈیش بورڈ (Dashboard)", "🥛 ڈیری اور دودھ ریکارڈ", "🐄 لائیو اسٹاک اخراجات", "🌾 فصل اور رقبہ مینجمنٹ"]
    )
    st.markdown("---")
    st.info("💡 **سسٹم اسٹیٹس:**\nآف لائن موڈ + کلاؤڈ سنک فعال ہے!")

# ---------------------------------------------------------
# 1. PROFESSIONAL DASHBOARD
# ---------------------------------------------------------
if menu == "📊 ڈیش بورڈ (Dashboard)":
    st.header("📊 فارم فنانشل ڈیش بورڈ")
    st.write("یہاں آپ کو اپنے پورے فارم کی آمدنی، خرچے اور منافع کا لائیو جائزہ ملے گا۔")
    
    milk_df = db.get_milk_records()
    live_df = db.get_livestock_records()
    crop_df = db.get_crop_records()
    
    total_milk_revenue = milk_df["total_amount"].sum() if not milk_df.empty else 0.0
    total_livestock_exp = live_df["amount"].sum() if not live_df.empty else 0.0
    total_crop_rev = crop_df["revenue"].sum() if not crop_df.empty else 0.0
    total_crop_exp = crop_df["expenses"].sum() if not crop_df.empty else 0.0
    
    total_revenue = total_milk_revenue + total_crop_rev
    total_expenses = total_livestock_exp + total_crop_exp
    net_profit = total_revenue - total_expenses
    
    # KPI Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🥛 کل دودھ آمدنی", f"PKR {total_milk_revenue:,.2f}")
    col2.metric("🐄 کل لائیو اسٹاک خرچے", f"PKR {total_livestock_exp:,.2f}")
    col3.metric("🌾 فصل کی کل آمدنی", f"PKR {total_crop_rev:,.2f}")
    col4.metric("💰 خالص تخمینہ منافع", f"PKR {net_profit:,.2f}")
    
    st.markdown("---")
    
    # Quick Summary Table
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🥛 حالیہ دودھ کے ریکارڈز")
        if not milk_df.empty:
            st.dataframe(milk_df.tail(5), use_container_width=True)
        else:
            st.info("ابھی تک کوئی دودھ کا ریکارڈ درج نہیں ہوا۔")
            
    with col_b:
        st.subheader("🐄 حالیہ لائیو اسٹاک اخراجات")
        if not live_df.empty:
            st.dataframe(live_df.tail(5), use_container_width=True)
        else:
            st.info("ابھی تک کوئی خرچہ درج نہیں ہوا۔")

# ---------------------------------------------------------
# 2. DAIRY MANAGER
# ---------------------------------------------------------
elif menu == "🥛 ڈیری اور دودھ ریکارڈ":
    st.header("🥛 ڈیری پروڈکشن اور دودھ کا حساب")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📝 نیا دودھ انٹری کریں")
        with st.form("milk_form"):
            entry_date = st.date_input("تاریخ", date.today())
            morning = st.number_input("صبح کا دودھ (Liters)", min_value=0.0, step=0.5)
            evening = st.number_input("شام کا دودھ (Liters)", min_value=0.0, step=0.5)
            home_use = st.number_input("گھر کا استعمال (Liters)", min_value=0.0, step=0.5)
            rate = st.number_input("فی لیٹر ریٹ (PKR)", min_value=0.0, step=1.0, value=200.0)
            
            submitted = st.form_submit_button("محفوظ کریں", use_container_width=True)
            if submitted:
                db.add_milk(entry_date, morning, evening, home_use, rate)
                st.success("✅ ریکارڈ کامیابی سے محفوظ ہو گیا!")
                st.rerun()
                
    with col2:
        st.subheader("📋 تمام دودھ کے ریکارڈز کی ہسٹری")
        df = db.get_milk_records()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 ایکسل کے لیے CSV ڈاؤن لوڈ کریں", csv, "milk_records.csv", "text/csv")
        else:
            st.info("ابھی تک کوئی ریکارڈ موجود نہیں ہے۔")

# ---------------------------------------------------------
# 3. LIVESTOCK EXPENSES
# ---------------------------------------------------------
elif menu == "🐄 لائیو اسٹاک اخراجات":
    st.header("🐄 لائیو اسٹاک اور جانوروں کے اخراجات")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📝 نیا خرچہ درج کریں")
        with st.form("live_form"):
            exp_date = st.date_input("تاریخ", date.today())
            item_name = st.text_input("آئٹم کا نام (مثلاً ونڈا، کھال، میڈیسن، بھوسا)")
            amount = st.number_input("کل رقم (PKR)", min_value=0.0, step=100.0)
            
            submitted = st.form_submit_button("خرچہ محفوظ کریں", use_container_width=True)
            if submitted:
                if item_name:
                    db.add_livestock(exp_date, item_name, amount)
                    st.success("✅ خرچہ کامیابی سے محفوظ ہو گیا!")
                    st.rerun()
                else:
                    st.warning("برائے مہربانی آئٹم کا نام درج کریں۔")
                
    with col2:
        st.subheader("📋 خرچوں کی تفصیلی ہسٹری")
        df = db.get_livestock_records()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 اخراجات CSV ڈاؤن لوڈ کریں", csv, "livestock_expenses.csv", "text/csv")
        else:
            st.info("ابھی تک کوئی خرچہ درج نہیں ہوا۔")

# ---------------------------------------------------------
# 4. CROP MANAGER
# ---------------------------------------------------------
elif menu == "🌾 فصل اور رقبہ مینجمنٹ":
    st.header("🌾 فصل، رقبہ اور زرعی آمدنی")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📝 فصل کا نیا ڈیٹا درج کریں")
        with st.form("crop_form"):
            crop_name = st.text_input("فصل کا نام (مثلاً گندم، مکئی، برسیم)")
            land_acres = st.number_input("رقبہ (Acre / ایکڑ)", min_value=0.0, step=0.5)
            expenses = st.number_input("کل اخراجات (بجائی، کھاد وغیرہ)", min_value=0.0, step=500.0)
            yield_qty = st.text_input("پیداوار (مثلاً 40 من)")
            revenue = st.number_input("کل آمدنی (بیچ کر جو ملی)", min_value=0.0, step=500.0)
            
            submitted = st.form_submit_button("فصل کا ریکارڈ محفوظ کریں", use_container_width=True)
            if submitted:
                if crop_name:
                    db.add_crop(crop_name, land_acres, expenses, yield_qty, revenue)
                    st.success("✅ فصل کا ریکارڈ محفوظ ہو گیا!")
                    st.rerun()
                else:
                    st.warning("برائے مہربانی فصل کا نام درج کریں۔")
                
    with col2:
        st.subheader("📋 فصلوں اور زمین کا ریکارڈ")
        df = db.get_crop_records()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 فصل ڈیٹا CSV ڈاؤن لوڈ کریں", csv, "crop_records.csv", "text/csv")
        else:
            st.info("ابھی تک کوئی فصل درج نہیں ہوئی۔")