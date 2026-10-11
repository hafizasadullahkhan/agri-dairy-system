import sqlite3

def add_milk_record(date, morning, evening, home_use, rate):
    # Kul kitna doodh becha gaya (Sold Liters)
    total_produced = morning + evening
    sold_liters = total_produced - home_use
    
    if sold_liters < 0:
        print("❌ Ghalti: Home use ka doodh kul doodh se zyada nahi ho sakta!")
        return

    # Total Income calculation
    total_income = sold_liters * rate

    # Database me record save karna
    conn = sqlite3.connect("agri_dairy.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO milk_records (date, morning_liters, evening_liters, home_use_liters, sold_liters, rate_per_liter, total_income)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date, morning, evening, home_use, sold_liters, rate, total_income))

    conn.commit()
    conn.close()

    print("\n✅ Doodh ka record kamyabi se save ho gaya hai!")
    print(f"📊 Becha gaya doodh: {sold_liters} Liters | Kul Aamdani: Rs. {total_income}\n")


def view_milk_records():
    conn = sqlite3.connect("agri_dairy.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM milk_records")
    records = cursor.fetchall()

    conn.close()

    if not records:
        print("\n⚠️ Koi record nahi mila!")
        return

    print("\n--- 🥛 DAILY MILK RECORDS ---")
    for row in records:
        print(f"ID: {row[0]} | Date: {row[1]} | Subah: {row[2]}L | Sham: {row[3]}L | Gharelu: {row[4]}L | Becha: {row[5]}L | Rate: Rs.{row[6]} | Total: Rs.{row[7]}")
    print("-----------------------------\n")


if __name__ == "__main__":
    # Test karne ke liye sample data enter kar rahe hain
    print("--- Doodh Ka Record Enter Karein ---")
    add_milk_record(date="2026-10-11", morning=25.0, evening=20.0, home_use=5.0, rate=180.0)
    
    # Records dekhne ke liye
    view_milk_records()