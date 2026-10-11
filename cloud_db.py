from supabase import create_client, Client

SUPABASE_URL = "https://ndsfjdfkspjykutiarpa.supabase.co"
SUPABASE_KEY = "sb_publishable_m20XDa3jFv6zS-FFTjQskg_8lUcq_"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 1. Milk Records Functions
def sync_add_milk(date, morning, evening, home_use, rate):
    total_milk = morning + evening
    sold_milk = total_milk - home_use
    total_amount = sold_milk * rate
    
    data = {
        "date": str(date),
        "morning": float(morning),
        "evening": float(evening),
        "home_use": float(home_use),
        "rate": float(rate),
        "sold_qty": float(sold_milk),
        "total_amount": float(total_amount)
    }
    response = supabase.table("milk_records").insert(data).execute()
    return response

def get_cloud_milk_records():
    response = supabase.table("milk_records").select("*").execute()
    return response.data


# 2. Livestock Expenses Functions
def sync_add_livestock(date, item_name, amount):
    data = {
        "date": str(date),
        "item_name": item_name,
        "amount": float(amount)
    }
    response = supabase.table("livestock_expenses").insert(data).execute()
    return response

def get_cloud_livestock_records():
    response = supabase.table("livestock_expenses").select("*").execute()
    return response.data


# 3. Crop Records Functions
def sync_add_crop(crop_name, land_acres, expenses, yield_qty, revenue):
    data = {
        "crop_name": crop_name,
        "land_acres": float(land_acres),
        "expenses": float(expenses),
        "yield_qty": yield_qty,
        "revenue": float(revenue)
    }
    response = supabase.table("crop_records").insert(data).execute()
    return response

def get_cloud_crop_records():
    response = supabase.table("crop_records").select("*").execute()
    return response.data