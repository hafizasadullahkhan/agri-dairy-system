import streamlit as st
import pandas as pd
from datetime import date
import cloud_db as db

st.set_page_config(
    page_title="Agri-Dairy Enterprise Manager",
    page_icon="🌾",
    layout="wide"
)

# کسٹم CSS ڈیزائن (کلائنٹ لیوب لک کے لیے)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 Agri-Dairy Enterprise Manager")
st.markdown("**پروفیشنل فارم مینجمنٹ اینڈ فنانشل ڈیش بورڈ**")
st.markdown("---")

# سائیڈ بار مینو
menu = st.sidebar.selectbox("🎯 نیویگیشن مینو", ["📊 ڈیش بورڈ (Dashboard)", "🥛 ڈیری اور دودھ ریکارڈ", "🐄 لائیو اسٹاک اخراجات", "🌾 فصل اور رقبہ مینجمنٹ"])

# ---------------------------------------------------------
# 1. PROFESSIONAL DASHBOARD
# ---------------------------------------------------------
if menu == "📊 ڈیش بورڈ (Dashboard)":
    st.subheader("📈 فارم کی مجموعی کارکردگی (Summary)")
    
    milk_df = db.get_milk_records()
    live_df = db.get_livestock_records()
    crop_df = db.get_crop_records()
    
    total_milk_revenue = milk_df["total_amount"].sum() if not milk_df.empty else 0.0
    total_livestock_exp = live_df["amount"].sum() if not live_df.empty else 0.0
    total_crop_rev = crop_df["revenue"].sum() if not crop_df.empty else 0.0
    total_crop_exp = crop_df["expenses"].sum() if not crop_df.empty else 0.0
    
    net_profit = (total_milk_revenue + total_crop_rev) - (total_livestock_exp + total_crop_exp)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🥛 کل دودھ آمدنی", f"PKR {total_milk_revenue:,.2f}")
    col2.metric("🐄 کل لائیو اسٹاک خرچے", f"PKR {total_livestock_exp:,.2f}")
    col3.metric("🌾 فصل کی آمدنی", f"PKR {total_crop_rev:,.2f}")
    col4.metric("💰 خالص تخمینہ منافع", f"PKR {net_profit:,.2f}")
    
    st.markdown("---")
    st.info("💡 یہ سسٹم مکمل طور پر آف لائن اور کلاؤڈ سنکڈ موڈ میں کام کر رہا ہے۔")

# ---------------------------------------------------------
# 2. DAIRY MANAGER
# ---------------------------------------------------------
elif menu == "🥛 ڈیری اور دودھ ریکارڈ":
    st.header("🥛 Dairy & Milk Production")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("نیا ریکارڈ درج کریں")
        entry_date = st.date_input("تاریخ", date.today())
        morning = st.number_input("صبح کا دودھ (Liters)", min_value=0.0, step=0.5)
        evening = st.number_input("شام کا دودھ (Liters)", min_value=0.0, step=0.5)
        home_use = st.number_input("گھر کا استعمال (Liters)", min_value=0.0, step=0.5)
        rate = st.number_input("فی لیٹر ریٹ (PKR)", min_value=0.0, step=1.0)
        
        if st.button("محفوظ کریں", type="primary"):
            db.add_milk(entry_date, morning, evening, home_use, rate)
            st.success("ریکارڈ کامیابی سے محفوظ ہو گیا!")
            st.rerun()
                
    with col2:
        st.subheader("تاریخی ریکارڈز")
        df = db.get_milk_records()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 ڈیٹا ڈاؤن لوڈ کریں (CSV)", csv, "milk_records.csv", "text/csv")
        else:
            st.info("کوئی ریکارڈ موجود نہیں ہے۔")

# ---------------------------------------------------------
# 3. LIVESTOCK EXPENSES
# ---------------------------------------------------------
elif menu == "🐄 لائیو اسٹاک اخراجات":
    st.header("🐄 Livestock Expenses")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("نیا خرچہ درج کریں")
        exp_date = st.date_input("تاریخ", date.today(), key="l_date")
        item_name = st.text_input("آئٹم کا نام (مثلاً ونڈا، کھال، میڈیسن)")
        amount = st.number_input("کل رقم (PKR)", min_value=0.0, step=100.0)
        
        if st.button("خرچہ محفوظ کریں", type="primary"):
            if item_name:
                db.add_livestock(exp_date, item_name, amount)
                st.success("خرچہ محفوظ ہو گیا!")
                st.rerun()
            else:
                st.warning("برائے مہربانی نام درج کریں۔")
                
    with col2:
        st.subheader("خرچوں کی ہسٹری")
        df = db.get_livestock_records()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 خرچے ڈاؤن لوڈ کریں (CSV)", csv, "livestock_expenses.csv", "text/csv")
        else:
            st.info("کوئی خرچہ موجود نہیں ہے۔")

# ---------------------------------------------------------
# 4. CROP MANAGER
# ---------------------------------------------------------
elif menu == "🌾 فصل اور رقبہ مینجمنٹ":
    st.header("🌾 Crop & Land Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("فصل کا ریکارڈ درج کریں")
        crop_name = st.text_input("فصل کا نام (گندم، کپاس وغیرہ)")
        land_acres = st.number_input("رقبہ (Acre)", min_value=0.0, step=0.5)
        expenses = st.number_input("کل اخراجات (PKR)", min_value=0.0, step=500.0)
        yield_qty = st.text_input("پیداوار (من/کلو)")
        revenue = st.number_input("کل آمدنی (PKR)", min_value=0.0, step=500.0)
        
        if st.button("فصل محفوظ کریں", type="primary"):
            if crop_name:
                db.add_crop(crop_name, land_acres, expenses, yield_qty, revenue)
                st.success("فصل کا ریکارڈ محفوظ ہو گیا!")
                st.rerun()
            else:
                st.warning("فصل کا نام لکھیں۔")
                
    with col2:
        st.subheader("فصلوں کا ریکارڈ")
        df = db.get_crop_records()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 فصل ڈیٹا ڈاؤن لوڈ کریں (CSV)", csv, "crop_records.csv", "text/csv")
        else:
            st.info("کوئی فصل درج نہیں ہوئی۔")