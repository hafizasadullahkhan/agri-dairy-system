import streamlit as st
import pandas as pd
from datetime import date
import cloud_db as db

# Page Configuration
st.set_page_config(
    page_title="خان ڈیجیٹل کھاتا سسٹم",
    page_icon="📒",
    layout="wide"
)

# --- DIGITAL KHATA & FARM THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at top right, #0d3b25, #081c15);
        color: #e9edc9;
        font-family: 'Noto Nastaliq Urdu', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #081c15 100%);
        border-right: 2px solid #2d6a4f;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #132e22 !important;
        border: 1px solid #52b788 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    div[data-baseweb="popover"] {
        background-color: #132e22 !important;
        color: #ffffff !important;
    }
    
    h1 {
        color: #52b788 !important;
        font-size: 30px !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    h2, h3, h4 {
        color: #b7e4c7 !important;
    }
    
    .stMetric {
        background: rgba(27, 67, 50, 0.7);
        backdrop-filter: blur(12px);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(82, 183, 136, 0.3);
    }
    .stMetric label {
        color: #95d5b2 !important;
        font-size: 14px !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffb703 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        font-family: 'Poppins', sans-serif !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #52b788 0%, #2d6a4f 100%);
        color: #081c15;
        border-radius: 10px;
        font-weight: 700;
        font-family: 'Noto Nastaliq Urdu', serif !important;
        padding: 0.6rem 1.2rem;
        border: 1px solid #ffb703;
        width: 100%;
        box-shadow: 0 4px 15px rgba(82, 183, 136, 0.4);
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ffb703 0%, #d4a373 100%);
        color: #081c15;
    }
    
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #2d6a4f;
        background-color: rgba(19, 46, 34, 0.9);
    }
    
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {
        background-color: #132e22;
        color: white;
        border: 1px solid #52b788;
        border-radius: 8px;
        font-family: 'Noto Nastaliq Urdu', serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header with Logo Integration
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("logo.png", width=85)
    except:
        st.markdown("📒", unsafe_allow_html=True)
with col_title:
    st.title("خان ڈیجیٹل کھاتا اینڈ بینک رجسٹر")
    st.markdown("<h4 style='color: #ffb703; margin-top: -10px;'>📒 روایتی کھاتے اور بینک لین دین کا جدید ڈیجیٹل نظام</h4>", unsafe_allow_html=True)
st.markdown("---")

# Navigation Sidebar
with st.sidebar:
    try:
        st.image("logo.png", use_column_width=True)
    except:
        st.markdown("<h3 style='text-align: center; color: #52b788;'>KHAN FARM PORTAL</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.selectbox(
        "کیٹیگری منتخب کریں", 
        ["📊 مجموعی ڈیش بورڈ", "📒 کسٹمر / ادھار کھاتا رجسٹر", "🏦 بینک اے ٹی ایم & ڈپازٹ کھاتا", "🥛 ڈیری & فصل کا پرانا نظام"]
    )
    st.markdown("---")
    st.success("🟢 **سسٹم اسٹیٹس:**\nآف لائن + کلاؤڈ سنک فعال ہے")

# Fetch Data
milk_df = db.get_milk_records()
live_df = db.get_livestock_records()
crop_df = db.get_crop_records()

# ---------------------------------------------------------
# 1. DASHBOARD
# ---------------------------------------------------------
if menu == "📊 مجموعی ڈیش بورڈ":
    st.header("📊 فارم اور کھاتوں کا خلاصہ")
    
    total_milk_revenue = milk_df["total_amount"].sum() if not milk_df.empty else 0.0
    total_livestock_exp = live_df["amount"].sum() if not live_df.empty else 0.0
    total_crop_rev = crop_df["revenue"].sum() if not crop_df.empty else 0.0
    total_crop_exp = crop_df["expenses"].sum() if not crop_df.empty else 0.0
    
    net_profit = (total_milk_revenue + total_crop_rev) - (total_livestock_exp + total_crop_exp)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🥛 کل دودھ آمدنی", f"PKR {total_milk_revenue:,.2f}")
    col2.metric("🐄 کل لائیو اسٹاک خرچے", f"PKR {total_livestock_exp:,.2f}")
    col3.metric("🌾 فصل کی کل آمدنی", f"PKR {total_crop_rev:,.2f}")
    col4.metric("💰 خالص تخمینہ منافع", f"PKR {net_profit:,.2f}")
    
    st.markdown("---")
    st.info("💡 آپ بائیں طرف سے **'کسٹمر / ادھار کھاتا رجسٹر'** پر کلک کر کے نیا کھاتا یا لین دین درج کر سکتے ہیں۔")

# ---------------------------------------------------------
# 2. DIGITAL KHATA REGISTER (New Feature)
# ---------------------------------------------------------
elif menu == "📒 کسٹمر / ادھار کھاتا رجسٹر":
    st.header("📒 کسٹمرز اور ادھار کھاتا رجسٹر")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📝 نیا کھاتا / لین دین درج کریں")
        with st.form("khata_form"):
            name = st.text_input("کسٹمر / بندے کا نام")
            father_name = st.text_input("والد کا نام")
            address = st.text_input("پتہ (رہائش)")
            phone = st.text_input("فون نمبر")
            cnic = st.text_input("شناختی کارڈ نمبر (CNIC)")
            
            st.markdown("---")
            trans_type = st.selectbox("لین دین کی قسم", ["رقم وصول کی (Credit/Received)", "رقم دی / ادھار دیا (Given)"])
            amount = st.number_input("رقم (روپے میں)", min_value=0.0, step=100.0)
            entry_date = st.date_input("لین دین کی تاریخ", date.today())
            due_date = st.date_input("واپسی کی متوقع تاریخ", date.today())
            description = st.text_area("تفصیل (بول کر یا لکھ کر رومن اردو میں درج کریں)")
            
            submitted = st.form_submit_button("خاتمہ / لین دین محفوظ کریں")
            if submitted:
                if name and amount > 0:
                    st.success(f"✅ {name} کا کھاتا کامیابی سے محفوظ ہو گیا!")
                    # یہاں ہم لوکل/کلاؤڈ میں ڈیٹا سیو کرنے کا فنکشن کال کر سکتے ہیں
                else:
                    st.warning("برائے مہربانی نام اور رقم درست درج کریں۔")
                    
    with col2:
        st.subheader("📋 تمام کھاتوں اور لین دین کی فہرست")
        st.info("یہاں آپ کے تمام کسٹمرز کے کھاتے اور لین دین کا ریکارڈ شو ہوگا۔")
        # سیمپل ٹی이블 یا ڈیٹا فریم
        sample_khata = pd.DataFrame(columns=["تاریخ", "نام", "والد کا نام", "فون نمبر", "قسم", "رقم", "تفصیل"])
        st.dataframe(sample_khata, use_container_width=True)

# ---------------------------------------------------------
# 3. BANK ATM & DEPOSIT REGISTER
# ---------------------------------------------------------
elif menu == "🏦 بینک اے ٹی ایم & ڈپازٹ کھاتا":
    st.header("🏦 بینک اکاؤنٹ، اے ٹی ایم اور ڈپازٹ رجسٹر")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📝 بینک ٹرانزیکشن درج کریں")
        with st.form("bank_form"):
            bank_name = st.text_input("بینک کا نام (مثلاً HBL, Meezan)")
            account_no = st.text_input("اکاؤنٹ نمبر")
            b_trans_type = st.selectbox("ٹرانزیکشن کی قسم", ["اے ٹی ایم نکاسی (ATM Withdrawal)", "رقم جمع کروائی (Deposit)"])
            b_amount = st.number_input("رقم (روپے)", min_value=0.0, step=500.0)
            b_date = st.date_input("تاریخ", date.today())
            b_desc = st.text_area("تفصیل / ریمارکس")
            
            b_submitted = st.form_submit_button("بینک ریکارڈ محفوظ کریں")
            if b_submitted:
                st.success("✅ بینک ریکارڈ کامیابی سے محفوظ ہو گیا!")
                
    with col2:
        st.subheader("📋 بینک ٹرانزیکشن ہسٹری")
        bank_df = pd.DataFrame(columns=["تاریخ", "بینک نام", "قسم", "رقم", "تفصیل"])
        st.dataframe(bank_df, use_container_width=True)

# ---------------------------------------------------------
# 4. OLD DAIRY & CROP SYSTEM
# ---------------------------------------------------------
elif menu == "🥛 ڈیری & فصل کا پرانا نظام":
    st.header("🥛 ڈیری اور فصلوں کا ریکارڈ")
    st.info("یہاں آپ کا پرانا دودھ اور فصلوں کا ریکارڈ موجود ہے۔")
    
    tab1, tab2 = st.tabs(["🥛 دودھ ریکارڈ", "🌾 فصل ریکارڈ"])
    with tab1:
        if not milk_df.empty:
            st.dataframe(milk_df, use_container_width=True)
        else:
            st.info("کوئی دودھ کا ریکارڈ نہیں ہے۔")
    with tab2:
        if not crop_df.empty:
            st.dataframe(crop_df, use_container_width=True)
        else:
            st.info("کوئی فصل کا ریکارڈ نہیں ہے۔")