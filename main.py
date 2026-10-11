import database
import dairy_manager
import livestock_manager
import crop_manager

def main_menu():
    # Sab se pehle database aur tables ensure karna
    database.init_db()

    while True:
        print("\n========================================")
        print("🌾🐄 SMART AGRI-DAIRY MANAGEMENT SYSTEM 🐄🌾")
        print("========================================")
        print("1. Doodh ka Record Darj Karein (Add Milk Entry)")
        print("2. Tamam Doodh ke Records Dekhein (View Milk Records)")
        print("3. Bhainson/Chaara ka Kharcha Darj Karein (Add Livestock Expense)")
        print("4. Tamam Akhrajaat Dekhein (View Livestock Expenses)")
        print("5. Fasal ka Record Darj Karein (Add Crop Record)")
        print("6. Tamam Faslon ka Record Dekhein (View Crop Records)")
        print("7. Program Band Karein (Exit)")
        print("========================================")

        choice = input("Apna option select karein (1-7): ")

        if choice == '1':
            print("\n--- 🥛 DOODH KA RECORD DARJ KAREIN ---")
            date = input("Tarikhe (Date YYYY-MM-DD): ")
            morning = float(input("Subah ka doodh (Liters): "))
            evening = input("Sham ka doodh (Liters): ")
            evening = float(evening) if evening else 0.0
            home_use = float(input("Ghar ke istemal ka doodh (Liters): "))
            rate = float(input("Fi Liter Rate (Rs): "))
            dairy_manager.add_milk_record(date, morning, evening, home_use, rate)

        elif choice == '2':
            dairy_manager.view_milk_records()

        elif choice == '3':
            print("\n--- 🐄 LIVESTOCK EXPENSE DARJ KAREIN ---")
            date = input("Tarikhe (Date YYYY-MM-DD): ")
            item_name = input("Cheez ka naam (Misaal: Vanda / Medicine): ")
            amount = float(input("Kul Raqam (Rs): "))
            livestock_manager.add_livestock_expense(date, item_name, amount)

        elif choice == '4':
            livestock_manager.view_livestock_expenses()

        elif choice == '5':
            print("\n--- 🌾 FASAL KA RECORD DARJ KAREIN ---")
            crop_name = input("Fasal ka naam (Misaal: Gandum): ")
            land_acres = float(input("Raqba (Acres me): "))
            expenses = float(input("Kul Kharcha (Rs): "))
            yield_qty = input("Pedawar (Misaal: 250 Mon): ")
            total_revenue = float(input("Mandi ki kul farokht/aamdani (Rs): "))
            crop_manager.add_crop_record(crop_name, land_acres, expenses, yield_qty, total_revenue)

        elif choice == '6':
            crop_manager.view_crop_records()

        elif choice == '7':
            print("\n👋 System band ho raha hai. Allah Hafiz!\n")
            break
        else:
            print("\n❌ Ghalat option! Baraye meharbani 1 se 7 ke darmiyan koi number chunein.\n")

if __name__ == "__main__":
    main_menu()