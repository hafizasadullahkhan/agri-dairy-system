import streamlit as st
import pandas as pd
from datetime import date
import cloud_db as db

# Page Configuration
st.set_page_config(
    page_title="Al-Madina Agri-Dairy Enterprise",
    page_icon="🌾",
    layout="wide"
)

# --- ULTIMATE LUXURY NASTALIQ & EMERALD FARM THEME ---
st.markdown("""
    <style>
    /* Import Google Noto Nastaliq Urdu Font */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

    /* Global Styling */
    .stApp {
        background: radial-gradient(circle at top right, #0d3b25, #081c15);
        color: #e9edc9;
        font-family: 'Noto Nastaliq Urdu', serif, sans-serif !important;
    }
    
    /* Sidebar Luxury Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #081c15 100%);
        border-left: 2px solid #2d6a4f;
    }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #d8f3dc !important;
        font-family: 'Noto Nastaliq Urdu', serif !important;
    }
    
    /* Headings with Gold & Emerald Glow */
    h1, h2, h3, h4 {
        color: #52b788 !important;
        font-weight: 700 !important;
        font-family: 'Noto Nastaliq Urdu', serif !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Luxury Glassmorphism Metric Cards */
    .stMetric {
        background: rgba(27, 67, 50, 0.6);
        backdrop-filter: blur(12px);
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(82, 183, 136, 0.2);
        transition: transform 0.3s ease;
    }
    .stMetric:hover {
        transform: translateY(-5px);
        border: 1px solid #52b788;
    }
    .stMetric label {
        color: #b7e4c7 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        font-family: 'Noto Nastaliq Urdu', serif !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 5px rgba(82, 183, 136, 0.5);
    }

    /* Professional Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%);
        color: #ffffff;
        border-radius: 10px;
        font-weight: 700;
        font-family: 'Noto Nastaliq Urdu', serif !important;
        padding: 0.6rem 1.2rem;
        border: 1px solid #52b788;
        width: 100%;
        box-shadow: 0 4px 15px rgba(45, 106, 79, 0.4);
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #52b788 0%, #2d6a4f 100%);
        color: #081c15;
        border: 1px solid #ffffff;
        box-shadow: 0 6px 20px rgba(82, 183, 136, 0.6);
    }
    
    /* Dataframes & Containers */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #2d6a4f;
        background-color: rgba(19, 46, 34, 0.8);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {
        background-color: #132e22;
        color: white;
        border: 1px solid #2d6a4f;
        border-radius: 8px;
        font-family: 'Noto Nastaliq Urdu', serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom Header with Logo Layout
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.markdown("🌾", unsafe_allow_html=True)
with col_title:
    st.title("البدر ایگری اینڈ ڈیری انٹرپرائز مینجر")
    st.markdown("### ✨ کلاؤڈ سنکڈ لیس دار فارم مینجمنٹ اینڈ فنانشل انٹیلی جنس سسٹم")
st.markdown("---")

# Navigation Sidebar with Professional Branding
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #52b788;'>🌟 فارم پورٹل</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.selectbox(
        "کیٹیگری منتخب کریں", 
        ["📊 ڈیش بورڈ (مجموعی جائزہ & گراف)", "🥛 ڈیری اور دودھ (Milk & Dairy)", "🐄 لائیو اسٹاک اخراجات", "🌾 فصل اور زرعی رقبہ"]
    )
    st.markdown("---")
    st.success("🟢 **سسٹم اسٹیٹس:**\nآف لائن موڈ + کلاؤڈ سنک فعال ہے")

# Fetch Data
milk_df = db.get_milk_records()
live_df = db.get_livestock_records()
crop_df = db.get_crop_records()

# ---------------------------------------------------------
# 1. LUXURY DASHBOARD
# ---------------------------------------------------------
if menu == "📊 ڈیش بورڈ (مجموعی جائزہ & گراف)":
    st.header("📊 فارم کا مالیاتی اور کارکردگی ڈیش بورڈ")
    
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
    
    # Visual Analytics & Charts
    st.subheader("📈 فنانشل تجزیہ اور لائیو گرافکس")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 🥛 دودھ کے مالیاتی اعدادوشمار")
        if not milk_df.empty:
            st.bar_chart(milk_df, x="date", y="total_amount")
        else:
            st.info("گراف کے لیے تاحال دودھ کا ڈیٹا موجود نہیں۔")
            
    with chart_col2:
        st.markdown("#### 🐄 لائیو اسٹاک اخراجات کا گراف")
        if not live_df.empty:
            st.bar_chart(live_df, x="date", y="amount")
        else:
            st.info("گراف کے لیے تاحال اخراجات کا ڈیٹا موجود نہیں۔")

# ---------------------------------------------------------
# 2. DAIRY MANAGER
# ---------------------------------------------------------
elif menu == "🥛 ڈیری اور دودھ (Milk & Dairy)":
    st.header("🥛 ڈیری پروڈکشن اور دودھ کا نظام")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📝 نیا دودھ ریکارڈ درج کریں")
        with st.form("milk_form"):
            entry_date = st.date_input("تاریخ", date.today())
            morning = st.number_input("صبح کا دودھ (لٹر)", min_value=0.0, step=0.5)
            evening = st.number_input("شام کا دودھ (لٹر)", min_value=0.0, step=0.5)
            home_use = st.number_input("گھر کا استعمال (لٹر)", min_value=0.0, step=0.5)
            rate = st.number_input("فی لیٹر ریٹ (روپے)", min_value=0.0, step=1.0, value=200.0)
            
            submitted = st.form_submit_button("محفوظ کریں")
            if submitted:
                db.add_milk(entry_date, morning, evening, home_use, rate)
                st.success("✅ ریکارڈ کامیابی سے محفوظ ہو گیا!")
                st.rerun()
                
    with col2:
        st.subheader("📋 ڈیری ریکارڈز کی ہسٹری")
        if not milk_df.empty:
            st.dataframe(milk_df, use_container_width=True)
            csv = milk_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 ڈیری ڈیٹا ایکسل میں ڈاؤن لوڈ کریں", csv, "milk_records.csv", "text/csv")
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
            item_name = st.text_input("آئٹم کا نام (ونڈا، میڈیسن، بھوسا وغیرہ)")
            amount = st.number_input("کل رقم (روپے)", min_value=0.0, step=100.0)
            
            submitted = st.form_submit_button("خرچہ محفوظ کریں")
            if submitted:
                if item_name:
                    db.add_livestock(exp_date, item_name, amount)
                    st.success("✅ خرچہ کامیابی سے محفوظ ہو گیا!")
                    st.rerun()
                else:
                    st.warning("برائے مہربانی آئٹم کا نام درج کریں۔")
                
    with col2:
        st.subheader("📋 اخراجات کی ہسٹری")
        if not live_df.empty:
            st.dataframe(live_df, use_container_width=True)
            csv = live_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 اخراجات ڈیٹا ڈاؤن لوڈ کریں", csv, "livestock_expenses.csv", "text/csv")
        else:
            st.info("ابھی تک کوئی خرچہ درج نہیں ہوا۔")

# ---------------------------------------------------------
# 4. CROP MANAGER
# ---------------------------------------------------------
elif menu == "🌾 فصل اور زرعی رقبہ":
    st.header("🌾 فصل، رقبہ اور زرعی آمدنی کا نظام")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📝 فصل کا نیا ڈیٹا درج کریں")
        with st.form("crop_form"):
            crop_name = st.text_input("فصل کا نام (گندم، مکئی، برسیم وغیرہ)")
            land_acres = st.number_input("رقبہ (ایکڑ)", min_value=0.0, step=0.5)
            expenses = st.number_input("کل اخراجات (کھاد، بیج وغیرہ)", min_value=0.0, step=500.0)
            yield_qty = st.text_input("پیداوار (مثلاً 40 من)")
            revenue = st.number_input("کل آمدنی (روپے)", min_value=0.0, step=500.0)
            
            submitted = st.form_submit_button("فصل کا ریکارڈ محفوظ کریں")
            if submitted:
                if crop_name:
                    db.add_crop(crop_name, land_acres, expenses, yield_qty, revenue)
                    st.success("✅ فصل کا ریکارڈ محفوظ ہو گیا!")
                    st.rerun()
                else:
                    st.warning("برائے مہربانی فصل کا نام درج کریں۔")
                
    with col2:
        st.subheader("📋 فصلوں کا ریکارڈ")
        if not crop_df.empty:
            st.dataframe(crop_df, use_container_width=True)
            csv = crop_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 فصل ڈیٹا ڈاؤن لوڈ کریں", csv, "crop_records.csv", "text/csv")
        else:
            st.info("ابھی تک کوئی فصل درج نہیں ہوئی۔")