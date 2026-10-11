import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import database
import dairy_manager
import livestock_manager
import crop_manager

# Database initialize karna
database.init_db()

class AgriDairyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Agri-Dairy Management System")
        self.root.geometry("900x650")
        self.root.config(bg="#f0f4f8")

        # Header Title
        title_label = tk.Label(root, text="🌾🐄 Smart Agri-Dairy Management System 🐄🌾", 
                               font=("Arial", 18, "bold"), bg="#2c3e50", fg="white", pady=10)
        title_label.pack(fill=tk.X)

        # Notebook (Tabs) create karna
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.tab_dairy = ttk.Frame(self.notebook)
        self.tab_livestock = ttk.Frame(self.notebook)
        self.tab_crop = ttk.Frame(self.notebook)
        self.tab_reports = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dairy, text=" 🥛 Doodh Entry ")
        self.notebook.add(self.tab_livestock, text=" 🐄 Livestock Kharcha ")
        self.notebook.add(self.tab_crop, text=" 🌾 Fasal Entry ")
        self.notebook.add(self.tab_reports, text=" 📊 Tamam Reports ")

        # Tabs ke andar widgets banana
        self.setup_dairy_tab()
        self.setup_livestock_tab()
        self.setup_crop_tab()
        self.setup_reports_tab()

    # ---------------- 1. DAIRY TAB ----------------
    def setup_dairy_tab(self):
        frame = tk.LabelFrame(self.tab_dairy, text=" Naya Doodh Record Darj Karein ", font=("Arial", 12, "bold"), padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(frame, text="Tarikhe (YYYY-MM-DD):", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dairy_date = tk.Entry(frame, font=("Arial", 10), width=25)
        self.dairy_date.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Subah ka Doodh (Liters):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dairy_morning = tk.Entry(frame, font=("Arial", 10), width=25)
        self.dairy_morning.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Sham ka Doodh (Liters):", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dairy_evening = tk.Entry(frame, font=("Arial", 10), width=25)
        self.dairy_evening.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Ghar ke Istemal ka Doodh (Liters):", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.dairy_home = tk.Entry(frame, font=("Arial", 10), width=25)
        self.dairy_home.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Fi Liter Rate (Rs):", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.dairy_rate = tk.Entry(frame, font=("Arial", 10), width=25)
        self.dairy_rate.grid(row=4, column=1, pady=5)

        btn_save_dairy = tk.Button(frame, text="Record Save Karein", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", command=self.save_dairy)
        btn_save_dairy.grid(row=5, column=0, columnspan=2, pady=20)

    def save_dairy(self):
        try:
            date = self.dairy_date.get()
            morning = float(self.dairy_morning.get() or 0)
            evening = float(self.dairy_evening.get() or 0)
            home_use = float(self.dairy_home.get() or 0)
            rate = float(self.dairy_rate.get() or 0)

            if not date:
                messagebox.showerror("Ghalti", "Baraye meharbani tarikhe darj karein!")
                return

            dairy_manager.add_milk_record(date, morning, evening, home_use, rate)
            messagebox.showinfo("Kamyabi", "Doodh ka record kamyabi se save ho gaya hai!")
            
            self.dairy_date.delete(0, tk.END)
            self.dairy_morning.delete(0, tk.END)
            self.dairy_evening.delete(0, tk.END)
            self.dairy_home.delete(0, tk.END)
            self.dairy_rate.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ghalti", "Baraye meharbani theek numerical values likhein!")

    # ---------------- 2. LIVESTOCK TAB ----------------
    def setup_livestock_tab(self):
        frame = tk.LabelFrame(self.tab_livestock, text=" Bhainson aur Chaara ka Kharcha Darj Karein ", font=("Arial", 12, "bold"), padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(frame, text="Tarikhe (YYYY-MM-DD):", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.live_date = tk.Entry(frame, font=("Arial", 10), width=25)
        self.live_date.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Cheez ka Naam (Vanda/Medicine):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.live_item = tk.Entry(frame, font=("Arial", 10), width=25)
        self.live_item.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Kul Raqam (Rs):", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.live_amount = tk.Entry(frame, font=("Arial", 10), width=25)
        self.live_amount.grid(row=2, column=1, pady=5)

        btn_save_live = tk.Button(frame, text="Kharcha Save Karein", font=("Arial", 11, "bold"), bg="#2980b9", fg="white", command=self.save_livestock)
        btn_save_live.grid(row=3, column=0, columnspan=2, pady=20)

    def save_livestock(self):
        try:
            date = self.live_date.get()
            item = self.live_item.get()
            amount = float(self.live_amount.get() or 0)

            if not date or not item:
                messagebox.showerror("Ghalti", "Tamam fields pur karna lazmi hain!")
                return

            livestock_manager.add_livestock_expense(date, item, amount)
            messagebox.showinfo("Kamyabi", "Kharcha kamyabi se save ho gaya hai!")

            self.live_date.delete(0, tk.END)
            self.live_item.delete(0, tk.END)
            self.live_amount.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ghalti", "Raqam me sirf numbers likhein!")

    # ---------------- 3. CROP TAB ----------------
    def setup_crop_tab(self):
        frame = tk.LabelFrame(self.tab_crop, text=" Fasal aur Zameen ka Record Darj Karein ", font=("Arial", 12, "bold"), padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(frame, text="Fasal ka Naam (Gandum/Kaptas):", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.crop_name = tk.Entry(frame, font=("Arial", 10), width=25)
        self.crop_name.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Raqba (Acres me):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.crop_acres = tk.Entry(frame, font=("Arial", 10), width=25)
        self.crop_acres.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Kul Kharcha (Rs):", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.crop_expenses = tk.Entry(frame, font=("Arial", 10), width=25)
        self.crop_expenses.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Pedawar (Misaal: 250 Mon):", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.crop_yield = tk.Entry(frame, font=("Arial", 10), width=25)
        self.crop_yield.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Mandi ki Kul Farokht/Aamdani (Rs):", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.crop_revenue = tk.Entry(frame, font=("Arial", 10), width=25)
        self.crop_revenue.grid(row=4, column=1, pady=5)

        btn_save_crop = tk.Button(frame, text="Fasal Record Save Karein", font=("Arial", 11, "bold"), bg="#d35400", fg="white", command=self.save_crop)
        btn_save_crop.grid(row=5, column=0, columnspan=2, pady=20)

    def save_crop(self):
        try:
            name = self.crop_name.get()
            acres = float(self.crop_acres.get() or 0)
            expenses = float(self.crop_expenses.get() or 0)
            yield_qty = self.crop_yield.get()
            revenue = float(self.crop_revenue.get() or 0)

            if not name:
                messagebox.showerror("Ghalti", "Fasal ka naam likhna lazmi hai!")
                return

            crop_manager.add_crop_record(name, acres, expenses, yield_qty, revenue)
            messagebox.showinfo("Kamyabi", "Fasal ka record kamyabi se save ho gaya hai!")

            self.crop_name.delete(0, tk.END)
            self.crop_acres.delete(0, tk.END)
            self.crop_expenses.delete(0, tk.END)
            self.crop_yield.delete(0, tk.END)
            self.crop_revenue.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ghalti", "Baraye meharbani theek numerical values likhein!")

    # ---------------- 4. REPORTS TAB ----------------
    def setup_reports_tab(self):
        frame = tk.Frame(self.tab_reports, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Refresh Button
        btn_refresh = tk.Button(frame, text="🔄 Tamam Reports Refresh/Dekhein", font=("Arial", 11, "bold"), bg="#8e44ad", fg="white", command=self.load_reports)
        btn_refresh.pack(pady=10)

        # Text Box to display records neatly
        self.report_text = tk.Text(frame, font=("Consolas", 10), bg="#1e1e2f", fg="#00ffcc", padx=10, pady=10)
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_reports(self):
        self.report_text.delete("1.0", tk.END)
        
        conn = sqlite3.connect("agri_dairy.db")
        cursor = conn.cursor()

        # 1. Milk Records
        self.report_text.insert(tk.END, "=== 🥛 DOODH KE RECORDS ===\n")
        cursor.execute("SELECT * FROM milk_records")
        milk_rows = cursor.fetchall()
        if not milk_rows:
            self.report_text.insert(tk.END, "Koi record mojood nahi.\n\n")
        else:
            for row in milk_rows:
                self.report_text.insert(tk.END, f"Tarikhe: {row[1]} | Subah: {row[2]}L | Sham: {row[3]}L | Becha: {row[5]}L | Total Aamdani: Rs.{row[7]}\n")
            self.report_text.insert(tk.END, "\n")

        # 2. Livestock Expenses
        self.report_text.insert(tk.END, "=== 🐄 LIVESTOCK AUR CHAARAY KE KHARCHE ===\n")
        cursor.execute("SELECT * FROM livestock_expenses")
        live_rows = cursor.fetchall()
        total_live_exp = 0
        if not live_rows:
            self.report_text.insert(tk.END, "Koi kharcha mojood nahi.\n\n")
        else:
            for row in live_rows:
                self.report_text.insert(tk.END, f"Tarikhe: {row[1]} | Item: {row[2]} | Raqam: Rs.{row[3]}\n")
                total_live_exp += row[3]
            self.report_text.insert(tk.END, f"-> Kul Livestock Kharcha: Rs. {total_live_exp}\n\n")

        # 3. Crop Records
        self.report_text.insert(tk.END, "=== 🌾 FASLON AUR ZAMEEN KE RECORDS ===\n")
        cursor.execute("SELECT * FROM crop_records")
        crop_rows = cursor.fetchall()
        if not crop_rows:
            self.report_text.insert(tk.END, "Koi fasal ka record mojood nahi.\n\n")
        else:
            for row in crop_rows:
                net_profit = row[5] - row[3]
                self.report_text.insert(tk.END, f"Fasal: {row[1]} | Raqba: {row[2]} Acres | Kharcha: Rs.{row[3]} | Aamdani: Rs.{row[5]} | Munafa: Rs.{net_profit}\n")
            self.report_text.insert(tk.END, "\n")

        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AgriDairyApp(root)
    root.mainloop()