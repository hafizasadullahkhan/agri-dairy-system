import sqlite3

def init_db():
    # Database file se connection
    conn = sqlite3.connect("agri_dairy.db")
    cursor = conn.cursor()

    # 1. Doodh ki rozana farokht aur pedawar ka table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milk_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            morning_liters REAL DEFAULT 0,
            evening_liters REAL DEFAULT 0,
            home_use_liters REAL DEFAULT 0,
            sold_liters REAL DEFAULT 0,
            rate_per_liter REAL DEFAULT 0,
            total_income REAL DEFAULT 0
        )
    ''')

    # 2. Chaare aur bhainson ke ikhrajat ka table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livestock_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            item_name TEXT NOT NULL,  -- Misaal: Vanda, Chara, Dawa
            amount REAL NOT NULL
        )
    ''')

    # 3. Faslon aur zameen ke ikhrajat/aamdani ka table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crop_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL,  -- Misaal: Gandum, Kaptas
            land_acres REAL NOT NULL,
            expenses REAL DEFAULT 0,   -- Beej, Diesel, Khaad ka kul kharcha
            yield_qty TEXT,           -- Pedawar (Misaal: 40 Moun)
            total_revenue REAL DEFAULT 0 -- Mandi ki farokht
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database aur tamam tables kamyabi se ban gaye hain!")

if __name__ == "__main__":
    init_db()