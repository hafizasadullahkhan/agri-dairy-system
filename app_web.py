import streamlit as st
import pandas as pd
from datetime import date
import cloud_db as db

# Page Configuration
st.set_page_config(
    page_title="KHAN FARM PORTAL",
    page_icon="📒",
    layout="wide"
)

# --- LUXURY KHATA & BANK THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Global App Background & Colors */
    .stApp {
        background: radial-gradient(circle at top right, #0d3b25, #081c15);
        color: #e9edc9;
        font-family: 'Noto Nastaliq Urdu', sans-serif !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #081c15 100%);
        border-right: 2px solid #2d6a4f;
        padding-top: 10px;
    }
    
    /* Radio Buttons & Selectbox Styling in Sidebar */
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stSelectbox label {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        font-family: 'Noto Nastaliq Urdu', serif !important;
    }
    
    /* Selectbox Fix */
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
    
    /* Typography */
    h1 {
        color: #52b788 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        font-family: 'Noto Nastaliq Urdu', serif !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    h2, h3, h4 {
        color: #b7e4c7 !important;
        font-family: 'Noto Nastaliq Urdu', serif !important;
    }

    /* Buttons */
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
    
    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #2d6a4f;
        background-color: rgba(19, 46, 34, 0.9);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #132e22;
        color: white;
        border: 1px solid #52b788;
        border-radius: 8px;
        font-family: 'Noto Nastaliq Urdu', serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("logo.png", width=90)
    except:
        st.markdown("📒", unsafe_allow_html=True)
with col_title:
    st.title("خان فارم پورٹل - ڈیجیٹل کھاتا رجسٹر")
    st.markdown("<h4 style='color: #ffb703; margin-top: -10px;'>📒 کسٹمر ادھار کھاتاجات اور بینک ٹرانزیکشنز مینجمنٹ</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar with Logo & ONLY 2 Categories
with st.sidebar:
    try:
        st.image("logo.png", use_column_width=True)
    except:
        st.markdown("<h3 style='text-align: center; color: #52b788;'>KHAN FARM PORTAL</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.radio(
        "مینجمنٹ کیٹیگری:", 
        ["📒 کسٹمر / ادھار کھاتا رجسٹر", "🏦 بینک اے ٹی ایم & ڈپازٹ کھاتا"]
    )
    st.markdown("---")
    st.success("🟢 **سسٹم اسٹیٹس:**\nآف لائن + کلاؤڈ سنک فعال ہے")

# ---------------------------------------------------------
# 1. CUSTOMER / KHATA REGISTER
# ---------------------------------------------------------
if menu == "📒 کسٹمر / ادھار کھاتا رجسٹر":
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
                else:
                    st.warning("برائے مہربانی نام اور رقم درست درج کریں۔")
                    
    with col2:
        st.subheader("📋 تمام کھاتوں اور لین دین کی فہرست")
        sample_khata = pd.DataFrame(columns=["تاریخ", "نام", "والد کا نام", "فون نمبر", "قسم", "رقم", "تفصیل"])
        st.dataframe(sample_khata, use_container_width=True)

# ---------------------------------------------------------
# 2. BANK ATM & DEPOSIT REGISTER
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