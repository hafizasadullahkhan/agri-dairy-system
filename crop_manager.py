import sqlite3

def add_crop_record(crop_name, land_acres, expenses, yield_qty, total_revenue):
    # Database se connect karna
    conn = sqlite3.connect("agri_dairy.db")
    cursor = conn.cursor()

    # Crop record insert karna
    cursor.execute('''
        INSERT INTO crop_records (crop_name, land_acres, expenses, yield_qty, total_revenue)
        VALUES (?, ?, ?, ?, ?)
    ''', (crop_name, land_acres, expenses, yield_qty, total_revenue))

    conn.commit()
    conn.close()

    # Net profit calculation
    net_profit = total_revenue - expenses
    print(f"\n✅ Fasal ka record kamyabi se save ho gaya! | Fasal: {crop_name} | Munafa (Profit): Rs. {net_profit}\n")


def view_crop_records():
    conn = sqlite3.connect("agri_dairy.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM crop_records")
    records = cursor.fetchall()

    conn.close()

    if not records:
        print("\n⚠️ Koi fasal ka record nahi mila!")
        return

    print("\n--- 🌾 CROP & FARMING RECORDS ---")
    for row in records:
        net_profit = row[5] - row[3]  # Revenue - Expenses
        print(f"ID: {row[0]} | Fasal: {row[1]} | Raqba: {row[2]} Acres | Kharcha: Rs.{row[3]} | Pedawar: {row[4]} | Aamdani: Rs.{row[5]} | Munafa: Rs.{net_profit}")
    print("----------------------------------\n")


if __name__ == "__main__":
    # Test karne ke liye sample data
    print("--- Fasal Ka Record Enter Karein ---")
    add_crop_record(crop_name="Gandum (Wheat)", land_acres=10.0, expenses=150000.0, yield_qty="250 Mon", total_revenue=400000.0)

    # Saari faslon ka record dekhne ke liye
    view_crop_records()