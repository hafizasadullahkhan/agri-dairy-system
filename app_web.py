import streamlit as st
import pandas as pd
from datetime import date
import cloud_db as db

st.set_page_config(
    page_page_title="Agri-Dairy System",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Agri-Dairy Management System")
st.subheader("کلاؤڈ سنکڈ زرعی و ڈیرَی فارم مینیجر")

# Navigation Menu
menu = st.sidebar.radio("مین مینو", ["🥛 Dairy Manager", "🐄 Livestock Expenses", "🌾 Crop Manager"])

# ---------------------------------------------------------
# 1. DAIRY MANAGER
# ---------------------------------------------------------
if menu == "🥛 Dairy Manager":
    st.header("🥛 Dairy & Milk Production")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("نیا ملحقہ ڈیٹا درج کریں")
        entry_date = st.date_input("تاریخ", date.today())
        morning = st.number_input("صبح کا دودھ (Liters)", min_value=0.0, step=0.5)
        evening = st.number_input("شام کا دودھ (Liters)", min_value=0.0, step=0.5)
        home_use = st.number_input("گھر کا استعمال (Liters)", min_value=0.0, step=0.5)
        rate = st.number_input("فی لیٹر ریٹ (PKR)", min_value=0.0, step=1.0)
        
        if st.button("کلاؤڈ پر سیو کریں", type="primary"):
            try:
                db.sync_add_milk(entry_date, morning, evening, home_use, rate)
                st.success("ڈیٹا کامیابی سے کلاؤڈ پر سیو ہو گیا!")
            except Exception as e:
                st.error(f"ایرر: {e}")
                
    with col2:
        st.subheader("کلاؤڈ سے لائیو ریکارڈز")
        try:
            records = db.get_cloud_milk_records()
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ابھی تک کوئی ریکارڈ موجود نہیں ہے۔")
        except Exception as e:
            st.error(f"ڈیٹا لوڈ کرنے میں مسئلہ: {e}")

# ---------------------------------------------------------
# 2. LIVESTOCK EXPENSES
# ---------------------------------------------------------
elif menu == "🐄 Livestock Expenses":
    st.header("🐄 Livestock & Animals Expenses")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("نیا خرچہ درج کریں")
        exp_date = st.date_input("تاریخ", date.today())
        item_name = st.text_input("آئٹم کا نام (مثلاً ونڈا، کھال، میڈیسن)")
        amount = st.number_input("کل رقم (PKR)", min_value=0.0, step=100.0)
        
        if st.button("خرچہ کلاؤڈ پر سیو کریں", type="primary"):
            if item_name != "":
                try:
                    db.sync_add_livestock(exp_date, item_name, amount)
                    st.success("خرچہ کلاؤڈ پر محفوظ ہو گیا!")
                except Exception as e:
                    st.error(f"ایرر: {e}")
            else:
                st.warning("برائے مہربانی آئٹم کا نام درج کریں۔")
                
    with col2:
        st.subheader("کلاؤڈ سے خرچوں کی ہسٹری")
        try:
            records = db.get_cloud_livestock_records()
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ابھی تک کوئی خرچہ درج نہیں ہوا ہے۔")
        except Exception as e:
            st.error(f"ڈیٹا لوڈ کرنے میں مسئلہ: {e}")

# ---------------------------------------------------------
# 3. CROP MANAGER
# ---------------------------------------------------------
elif menu == "🌾 Crop Manager":
    st.header("🌾 Crop & Land Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("فصل کا ڈیٹا درج کریں")
        crop_name = st.text_input("فصل کا نام (مثلاً گندم، مکی، کپاس)")
        land_acres = st.number_input("رقبہ (Acre)", min_value=0.0, step=0.5)
        expenses = st.number_input("کل اخراجات (PKR)", min_value=0.0, step=500.0)
        yield_qty = st.text_input("پیداوار (مثلاً 40 من)")
        revenue = st.number_input("کل آمدنی (PKR)", min_value=0.0, step=500.0)
        
        if st.button("فصل کا ریکارڈ سیو کریں", type="primary"):
            if crop_name != "":
                try:
                    db.sync_add_crop(crop_name, land_acres, expenses, yield_qty, revenue)
                    st.success("فصل کا ریکارڈ کلاؤڈ پر سیو ہو گیا!")
                except Exception as e:
                    st.error(f"ایرر: {e}")
            else:
                st.warning("برائے مہربانی فصل کا نام درج کریں۔")
                
    with col2:
        st.subheader("کلاؤڈ سے فصلوں کا ریکارڈ")
        try:
            records = db.get_cloud_crop_records()
            if records:
                df = pd.DataFrame(records)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ابھی تک کوئی فصل درج نہیں ہوئی۔")
        except Exception as e:
            st.error(f"ڈیٹا لوڈ کرنے میں مسئلہ: {e}")