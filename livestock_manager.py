import sqlite3

def add_livestock_expense(date, item_name, amount):
    # Database se connect karna
    conn = sqlite3.connect("agri_dairy.db")
    cursor = conn.cursor()

    # Expense insert karna
    cursor.execute('''
        INSERT INTO livestock_expenses (date, item_name, amount)
        VALUES (?, ?, ?)
    ''', (date, item_name, amount))

    conn.commit()
    conn.close()

    print(f"\n✅ Kharcha kamyabi se save ho gaya! | Item: {item_name} | Amount: Rs. {amount}\n")


def view_livestock_expenses():
    conn = sqlite3.connect("agri_dairy.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM livestock_expenses")
    records = cursor.fetchall()

    conn.close()

    if not records:
        print("\n⚠️ Koi kharcha record nahi mila!")
        return

    print("\n--- 🐄 LIVESTOCK & FEED EXPENSES ---")
    total_expense = 0
    for row in records:
        print(f"ID: {row[0]} | Date: {row[1]} | Item: {row[2]} | Amount: Rs.{row[3]}")
        total_expense += row[3]
    print(f"------------------------------------")
    print(f"💰 Kul Kharcha (Total Expense): Rs. {total_expense}\n")


if __name__ == "__main__":
    # Test karne ke liye sample data
    print("--- Bhainson Aur Chaare Ka Kharcha Enter Karein ---")
    add_livestock_expense(date="2026-10-11", item_name="Vanda (Feed Bag)", amount=3500.0)
    add_livestock_expense(date="2026-10-11", item_name="Doctor / Medicine", amount=1200.0)

    # All expenses dekhne ke liye
    view_livestock_expenses()