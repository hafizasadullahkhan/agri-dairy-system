import sqlite3
import pandas as pd
from datetime import date
from supabase import create_client, Client

SUPABASE_URL = "https://ndsfjdfkspjykutiarpa.supabase.co"
SUPABASE_KEY = "sb_publishable_m20XDa3jFv6zS-FFTjQskg_8lUcq_"

# Supabase Client (اگر انٹرنیٹ ہو تو)
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    supabase = None

# --- LOCAL SQLITE SETUP (آف لائن ڈیٹا بیس) ---
def init_local_db():
    conn = sqlite3.connect("local_farm.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS milk_records (
                        date TEXT, morning REAL, evening REAL, home_use REAL, rate REAL, sold_qty REAL, total_amount REAL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS livestock_expenses (
                        date TEXT, item_name TEXT, amount REAL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS crop_records (
                        crop_name TEXT, land_acres REAL, expenses REAL, yield_qty TEXT, revenue REAL)''')
    
    conn.commit()
    conn.close()

init_local_db()

# --- 1. MILK FUNCTIONS ---
def add_milk(date_val, morning, evening, home_use, rate):
    total_milk = morning + evening
    sold_milk = total_milk - home_use
    total_amount = sold_milk * rate
    
    # پہلے لوکل سیو کریں (آف لائن سپورٹ)
    conn = sqlite3.connect("local_farm.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO milk_records VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (str(date_val), morning, evening, home_use, rate, sold_milk, total_amount))
    conn.commit()
    conn.close()
    
    # کوشش کریں کلاؤڈ پر بھی چلا جائے
    if supabase:
        try:
            data = {
                "date": str(date_val), "morning": float(morning), "evening": float(evening),
                "home_use": float(home_use), "rate": float(rate), "sold_qty": float(sold_milk), "total_amount": float(total_amount)
            }
            supabase.table("milk_records").insert(data).execute()
        except:
            pass

def get_milk_records():
    conn = sqlite3.connect("local_farm.db")
    df = pd.read_sql("SELECT * FROM milk_records", conn)
    conn.close()
    return df

# --- 2. LIVESTOCK EXPENSES FUNCTIONS ---
def add_livestock(date_val, item_name, amount):
    conn = sqlite3.connect("local_farm.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO livestock_expenses VALUES (?, ?, ?)", (str(date_val), item_name, amount))
    conn.commit()
    conn.close()
    
    if supabase:
        try:
            data = {"date": str(date_val), "item_name": item_name, "amount": float(amount)}
            supabase.table("livestock_expenses").insert(data).execute()
        except:
            pass

def get_livestock_records():
    conn = sqlite3.connect("local_farm.db")
    df = pd.read_sql("SELECT * FROM livestock_expenses", conn)
    conn.close()
    return df

# --- 3. CROP RECORDS FUNCTIONS ---
def add_crop(crop_name, land_acres, expenses, yield_qty, revenue):
    conn = sqlite3.connect("local_farm.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO crop_records VALUES (?, ?, ?, ?, ?)", (crop_name, land_acres, expenses, yield_qty, revenue))
    conn.commit()
    conn.close()
    
    if supabase:
        try:
            data = {"crop_name": crop_name, "land_acres": float(land_acres), "expenses": float(expenses), "yield_qty": yield_qty, "revenue": float(revenue)}
            supabase.table("crop_records").insert(data).execute()
        except:
            pass

def get_crop_records():
    conn = sqlite3.connect("local_farm.db")
    df = pd.read_sql("SELECT * FROM crop_records", conn)
    conn.close()
    return df