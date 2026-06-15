import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
from datetime import datetime, timedelta

# --- COMPLIANT PROFESSIONAL & COOL STYLING CONFIGURATION ---
COLOR_BG_DARK = "#0F172A"  # Deep Obsidian Slate Blue (Main Window Background)
COLOR_SURFACE_NAVY = "#1E293B"  # Premium Soft Navy (Card Panels & Widgets)
COLOR_PRIMARY_TEAL = "#0EA5E9"  # Vibrant Cyber Teal (Buttons, Titles, Highlight Accents)
COLOR_TEXT_LIGHT = "#F8FAFC"  # Crisp White Mint Text
COLOR_TEXT_MUTED = "#94A3B8"  # Industrial Muted Gray for subtitles/borders
COLOR_GREEN_ACTIVE = "#10B981"  # Mint Green for Active States
COLOR_RED_DELETE = "#EF4444"  # Deep Crimson Red for Purge/Exits
COLOR_SECONDARY_TEAL = "#238636" #

FONT_FAMILY = "Tahoma"


# --- DATABASE SETUP & INITIALIZATION ---
def initialize_database():
    """Sets up SQLite database and injects 20 preloaded realistic records if empty."""
    conn = sqlite3.connect("clinic_records.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            created_date DATE NOT NULL,
            status TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    # Check if database needs 20 initial sample records
    cursor.execute("SELECT COUNT(*) FROM records")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("Alhaji Bangura", "Male", 68, "2026-06-12", "Active", "+232-77-555111", "High Priority (Triage)"),
            ("Fatmata Kamara", "Female", 4, "2026-06-13", "Active", "+232-33-444222", "High Priority (Triage)"),
            ("Mohamed Mansaray", "Male", 29, "2026-06-10", "Active", "+232-88-111222", "Standard"),
            ("Sia Koroma", "Female", 62, "2026-06-01", "Active", "+232-76-999888", "High Priority (Triage)"),
            ("Amadu Jalloh", "Male", 3, "2026-05-15", "Pending", "+232-77-333444", "High Priority (Triage)"),
            ("Mariama Conteh", "Female", 18, "2026-06-13", "Active", "+232-30-555666", "Standard"),
            ("Samuel Turay", "Male", 74, "2026-04-20", "Inactive", "+232-76-222333", "High Priority (Triage)"),
            ("Zainab Sesay", "Female", 22, "2026-06-11", "Active", "+232-88-777666", "Standard"),
            ("Osman Fofanah", "Male", 5, "2026-06-13", "Active", "+232-77-888999", "High Priority (Triage)"),
            ("Isatu Kanu", "Female", 45, "2026-06-05", "Pending", "+232-33-111000", "Standard"),
            ("Kadiatu Kargbo", "Female", 61, "2026-06-12", "Active", "+232-76-444555", "High Priority (Triage)"),
            ("Bintu Dumbuya", "Female", 2, "2026-06-09", "Active", "+232-88-333222", "High Priority (Triage)"),
            ("Emmanuel Cole", "Male", 35, "2026-05-28", "Inactive", "+232-30-999111", "Standard"),
            ("Sallieu Barrie", "Male", 66, "2026-06-13", "Active", "+232-77-222444", "High Priority (Triage)"),
            ("Rebecca Williams", "Female", 55, "2026-06-02", "Active", "+232-76-888111", "Standard"),
            ("Mustapha Kallon", "Male", 1, "2026-06-13", "Active", "+232-33-777333", "High Priority (Triage)"),
            ("Grace Taylor", "Female", 67, "2026-03-14", "Inactive", "+232-88-444555", "High Priority (Triage)"),
            ("Abu Bakar Kamara", "Male", 24, "2026-06-07", "Pending", "+232-77-111555", "Standard"),
            ("Hawa Bangura", "Female", 31, "2026-06-12", "Active", "+232-76-333999", "Standard"),
            ("Julius Dumbuya", "Male", 70, "2026-06-13", "Active", "+232-33-888222", "High Priority (Triage)")
        ]
        cursor.executemany("""
            INSERT INTO records (full_name, gender, age, created_date, status, contact_info, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        conn.commit()
    conn.close()


# --- MAIN APPLICATION CLASS CONTAINER ---
class ApplicationToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Clinic Information Desk & Triage Dashboard")
        self.geometry("1100x700")
        self.configure(bg=COLOR_BG_DARK)

        # Centralizing Style adjustments for Treeviews
        self.custom_tree_style()

        # Frame View Controller State
        self.login_frame = None
        self.dashboard_frame = None

        # Open up Auth Gate
        self.show_login_screen()

    def custom_tree_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=COLOR_SURFACE_NAVY,
                        foreground=COLOR_TEXT_LIGHT,
                        fieldbackground=COLOR_SURFACE_NAVY,
                        font=(FONT_FAMILY, 9),
                        rowheight=26)
        style.configure("Treeview.Heading",
                        background=COLOR_PRIMARY_TEAL,
                        foreground=COLOR_TEXT_LIGHT,
                        font=(FONT_FAMILY, 9, "bold"))
        style.map("Treeview",
                  background=[('selected', COLOR_SECONDARY_TEAL if 'COLOR_SECONDARY_TEAL' in globals() else "#0284C7")])

    def show_login_screen(self):
        if self.dashboard_frame:
            self.dashboard_frame.pack_forget()
        self.login_frame = LoginFrame(self)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def login_success(self):
        self.login_frame.pack_forget()
        self.dashboard_frame = DashboardFrame(self)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)


# --- LOGIN SCREEN WORKFLOW COMPONENT ---
class LoginFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG_DARK)
        self.parent = parent

        # Center Card Shell
        card = tk.Frame(self, bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID, highlightbackground=COLOR_TEXT_MUTED)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=420)

        # Header Badge
        lbl_title = tk.Label(card, text="CLINIC SYSTEM LOGIN", font=(FONT_FAMILY, 16, "bold"), fg=COLOR_PRIMARY_TEAL,
                             bg=COLOR_SURFACE_NAVY)
        lbl_title.pack(pady=(35, 5))

        lbl_sub = tk.Label(card, text="Authorized Medical Personnel Only", font=(FONT_FAMILY, 9, "italic"),
                           fg=COLOR_TEXT_MUTED, bg=COLOR_SURFACE_NAVY)
        lbl_sub.pack(pady=(0, 25))

        # Entry Forms Container
        form_frame = tk.Frame(card, bg=COLOR_SURFACE_NAVY)
        form_frame.pack(fill=tk.X, padx=35)

        tk.Label(form_frame, text="Username / Email:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).pack(anchor=tk.W, pady=2)
        self.ent_user = tk.Entry(form_frame, font=(FONT_FAMILY, 11), bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT,
                                 insertbackground=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID)
        self.ent_user.pack(fill=tk.X, ipady=5, pady=(0, 15))
        self.ent_user.insert(0, "admin")  # Convenience preset for examiner

        tk.Label(form_frame, text="Secure Password:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).pack(anchor=tk.W, pady=2)
        self.ent_pass = tk.Entry(form_frame, show="*", font=(FONT_FAMILY, 11), bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT,
                                 insertbackground=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID)
        self.ent_pass.pack(fill=tk.X, ipady=5, pady=(0, 20))
        self.ent_pass.insert(0, "password")  # Convenience preset for examiner

        # Action Triggers
        btn_login = tk.Button(card, text="SECURE ACCESS", font=(FONT_FAMILY, 11, "bold"), bg=COLOR_PRIMARY_TEAL,
                              fg=COLOR_TEXT_LIGHT, activebackground=COLOR_GREEN_ACTIVE,
                              activeforeground=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", command=self.process_auth)
        btn_login.pack(fill=tk.X, padx=35, ipady=8, pady=5)

        btn_forgot = tk.Button(card, text="Forgot Password Routine?", font=(FONT_FAMILY, 9, "underline"),
                               bg=COLOR_SURFACE_NAVY, fg=COLOR_TEXT_MUTED, activebackground=COLOR_SURFACE_NAVY,
                               activeforeground=COLOR_PRIMARY_TEAL, bd=0, cursor="hand2", command=self.forgot_password)
        btn_forgot.pack(pady=5)

    def process_auth(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()

        if u == "admin" and p == "password":
            self.parent.login_success()
        else:
            messagebox.showerror("Access Denied", "Invalid administrative username token or decryption password key.")

    def forgot_password(self):
        messagebox.showinfo("Security Assistance",
                            "Please contact the system administrator or Group 8 to reset your local database credentials.")


# --- DASHBOARD & ANALYTICAL WORKSPACE COMPONENT ---
class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG_DARK)
        self.parent = parent

        self.build_top_bar()

        # Master Workspace Layout Columns Split
        self.workspace = tk.Frame(self, bg=COLOR_BG_DARK, padx=15, pady=10)
        self.workspace.pack(fill=tk.BOTH, expand=True)

        self.left_panel = tk.Frame(self.workspace, bg=COLOR_BG_DARK)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.right_panel = tk.Frame(self.workspace, bg=COLOR_BG_DARK, width=320)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_panel.pack_propagate(False)

        self.build_filter_card()
        self.build_treeview_card()
        self.build_operational_form()

        self.load_data_grid()

    def build_top_bar(self):
        top_bar = tk.Frame(self, bg=COLOR_SURFACE_NAVY, height=65)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        lbl_title = tk.Label(top_bar, text="INTELLIGENT HEALTH INFRASTRUCTURE DASHBOARD",
                             font=(FONT_FAMILY, 13, "bold"), fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY)
        lbl_title.pack(side=tk.LEFT, padx=15, pady=10)

        btn_logout = tk.Button(top_bar, text="LOGOUT APP", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_RED_DELETE,
                               fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", padx=15,
                               command=self.parent.show_login_screen)
        btn_logout.pack(side=tk.RIGHT, padx=15, pady=18)

    def build_filter_card(self):
        card = tk.LabelFrame(self.left_panel, text=" Search & Dynamic Advanced Filters Matrix ",
                             font=(FONT_FAMILY, 10, "bold"), fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1,
                             relief=tk.SOLID)
        card.pack(fill=tk.X, pady=(0, 10), ipady=5)

        # Row 1 Queries
        tk.Label(card, text="Search Term:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=0, column=0, padx=8, pady=5, sticky=tk.W)
        self.ent_search = tk.Entry(card, font=(FONT_FAMILY, 10), bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1,
                                   relief=tk.SOLID, insertbackground=COLOR_TEXT_LIGHT)
        self.ent_search.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_data_grid())

        tk.Label(card, text="Gender Drop:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=0, column=2, padx=8, pady=5, sticky=tk.W)
        self.cmb_gender = ttk.Combobox(card, values=["All", "Male", "Female"], state="readonly", width=12)
        self.cmb_gender.current(0)
        self.cmb_gender.grid(row=0, column=3, padx=5, pady=5)
        self.cmb_gender.bind("<<ComboboxSelected>>", lambda e: self.load_data_grid())

        # Row 2 Queries
        tk.Label(card, text="Status Group:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=1, column=0, padx=8, pady=5, sticky=tk.W)
        self.cmb_status = ttk.Combobox(card, values=["All", "Active", "Inactive", "Pending"], state="readonly",
                                       width=15)
        self.cmb_status.current(0)
        self.cmb_status.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.cmb_status.bind("<<ComboboxSelected>>", lambda e: self.load_data_grid())

        tk.Label(card, text="Date Interval:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=1, column=2, padx=8, pady=5, sticky=tk.W)
        self.cmb_date = ttk.Combobox(card, values=["All Dates", "Daily (Today)", "Weekly (7 Days)", "Monthly (30 Days)",
                                                   "Yearly (365 Days)"], state="readonly", width=16)
        self.cmb_date.current(0)
        self.cmb_date.grid(row=1, column=3, padx=5, pady=5)
        self.cmb_date.bind("<<ComboboxSelected>>", lambda e: self.load_data_grid())

        card.columnconfigure(1, weight=1)

    def build_treeview_card(self):
        card = tk.Frame(self.left_panel, bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID)
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columns = ("id", "name", "gender", "age", "date", "status", "contact", "priority")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", selectmode="browse")

        # Format Mappings Header Lines
        headings = {"id": "ID", "name": "Patient Full Name", "gender": "Gender", "age": "Age", "date": "Date Created",
                    "status": "Status", "contact": "Contact Info", "priority": "Priority Assignment"}
        widths = {"id": 45, "name": 160, "gender": 65, "age": 45, "date": 95, "status": 75, "contact": 110,
                  "priority": 130}

        for col in columns:
            self.tree.heading(col, text=headings[col], anchor=tk.W)
            self.tree.column(col, width=widths[col], stretch=True if col in ["name", "priority"] else False)

        scroll = ttk.Scrollbar(card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self.on_record_selected)

    def build_operational_form(self):
        card = tk.LabelFrame(self.left_panel, text=" Quick Registry Intake Operations Console ",
                             font=(FONT_FAMILY, 10, "bold"), fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1,
                             relief=tk.SOLID)
        card.pack(fill=tk.X)

        # Row 1 Entry Prompts
        tk.Label(card, text="Name:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=0, column=0, padx=6, pady=5, sticky=tk.W)
        self.form_name = tk.Entry(card, bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID)
        self.form_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        tk.Label(card, text="Gender:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=0, column=2, padx=6, pady=5, sticky=tk.W)
        self.form_gender = ttk.Combobox(card, values=["Male", "Female", "Other"], state="readonly", width=10)
        self.form_gender.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(card, text="Age:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=0, column=4, padx=6, pady=5, sticky=tk.W)
        self.form_age = tk.Entry(card, width=6, bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID)
        self.form_age.grid(row=0, column=5, padx=5, pady=5)

        # Row 2 Entry Prompts
        tk.Label(card, text="Contact:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=1, column=0, padx=6, pady=5, sticky=tk.W)
        self.form_contact = tk.Entry(card, bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID)
        self.form_contact.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        tk.Label(card, text="Status:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=1, column=2, padx=6, pady=5, sticky=tk.W)
        self.form_status = ttk.Combobox(card, values=["Active", "Inactive", "Pending"], state="readonly", width=10)
        self.form_status.grid(row=1, column=3, padx=5, pady=5)

        # Grid Operations Command Rows
        btn_box = tk.Frame(card, bg=COLOR_SURFACE_NAVY)
        btn_box.grid(row=2, column=0, columnspan=6, pady=8, padx=5, sticky=tk.EW)

        tk.Button(btn_box, text="➕ Add Intake Record", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_PRIMARY_TEAL,
                  fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", width=18, command=self.add_record).pack(side=tk.LEFT,
                                                                                                     padx=3, ipady=4)
        tk.Button(btn_box, text="🔄 Toggle Priority", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_SURFACE_NAVY,
                  fg=COLOR_PRIMARY_TEAL, bd=1, relief=tk.SOLID, cursor="hand2", width=15,
                  command=self.toggle_priority).pack(side=tk.LEFT, padx=3, ipady=4)
        tk.Button(btn_box, text="🧹 Clear Fields", font=(FONT_FAMILY, 9, "bold"), bg="#475569", fg=COLOR_TEXT_LIGHT,
                  bd=0, cursor="hand2", width=12, command=self.clear_fields).pack(side=tk.LEFT, padx=3, ipady=4)
        tk.Button(btn_box, text="❌ Delete Patient", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_RED_DELETE,
                  fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", width=15, command=self.delete_record).pack(side=tk.RIGHT,
                                                                                                        padx=3, ipady=4)

        card.columnconfigure(1, weight=1)

    def build_treeview_card(self):
        card = tk.Frame(self.left_panel, bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID)
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columns = ("id", "name", "gender", "age", "date", "status", "contact", "priority")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", selectmode="browse")

        headings = {"id": "ID", "name": "Patient Full Name", "gender": "Gender", "age": "Age", "date": "Date Created",
                    "status": "Status", "contact": "Contact Info", "priority": "Priority Assignment"}
        widths = {"id": 45, "name": 160, "gender": 65, "age": 45, "date": 95, "status": 75, "contact": 110,
                  "priority": 130}

        for col in columns:
            self.tree.heading(col, text=headings[col], anchor=tk.W)
            self.tree.column(col, width=widths[col], stretch=True if col in ["name", "priority"] else False)

        scroll = ttk.Scrollbar(card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self.on_record_selected)

    def build_filter_card(self):
        card = tk.LabelFrame(self.left_panel, text=" Search & Dynamic Advanced Filters Matrix ",
                             font=(FONT_FAMILY, 10, "bold"), fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1,
                             relief=tk.SOLID)
        card.pack(fill=tk.X, pady=(0, 10), ipady=5)

        tk.Label(card, text="Search Term:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=0, column=0, padx=8, pady=5, sticky=tk.W)
        self.ent_search = tk.Entry(card, font=(FONT_FAMILY, 10), bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1,
                                   relief=tk.SOLID, insertbackground=COLOR_TEXT_LIGHT)
        self.ent_search.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_data_grid())

        tk.Label(card, text="Gender Drop:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=0, column=2, padx=8, pady=5, sticky=tk.W)
        self.cmb_gender = ttk.Combobox(card, values=["All", "Male", "Female"], state="readonly", width=12)
        self.cmb_gender.current(0)
        self.cmb_gender.grid(row=0, column=3, padx=5, pady=5)
        self.cmb_gender.bind("<<ComboboxSelected>>", lambda e: self.load_data_grid())

        tk.Label(card, text="Status Group:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=1, column=0, padx=8, pady=5, sticky=tk.W)
        self.cmb_status = ttk.Combobox(card, values=["All", "Active", "Inactive", "Pending"], state="readonly",
                                       width=15)
        self.cmb_status.current(0)
        self.cmb_status.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.cmb_status.bind("<<ComboboxSelected>>", lambda e: self.load_data_grid())

        tk.Label(card, text="Date Interval:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_SURFACE_NAVY).grid(row=1, column=2, padx=8, pady=5, sticky=tk.W)
        self.cmb_date = ttk.Combobox(card, values=["All Dates", "Daily (Today)", "Weekly (7 Days)", "Monthly (30 Days)",
                                                   "Yearly (365 Days)"], state="readonly", width=16)
        self.cmb_date.current(0)
        self.cmb_date.grid(row=1, column=3, padx=5, pady=5)
        self.cmb_date.bind("<<ComboboxSelected>>", lambda e: self.load_data_grid())

        card.columnconfigure(1, weight=1)

    def build_operational_form(self):
        card = tk.LabelFrame(self.left_panel, text=" Quick Registry Intake Operations Console ",
                             font=(FONT_FAMILY, 10, "bold"), fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1,
                             relief=tk.SOLID)
        card.pack(fill=tk.X)

        tk.Label(card, text="Name:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=0, column=0, padx=6, pady=5, sticky=tk.W)
        self.form_name = tk.Entry(card, bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID,
                                  insertbackground=COLOR_TEXT_LIGHT)
        self.form_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        tk.Label(card, text="Gender:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=0, column=2, padx=6, pady=5, sticky=tk.W)
        self.form_gender = ttk.Combobox(card, values=["Male", "Female", "Other"], state="readonly", width=10)
        self.form_gender.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(card, text="Age:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=0, column=4, padx=6, pady=5, sticky=tk.W)
        self.form_age = tk.Entry(card, width=6, bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID,
                                 insertbackground=COLOR_TEXT_LIGHT)
        self.form_age.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(card, text="Contact:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=1, column=0, padx=6, pady=5, sticky=tk.W)
        self.form_contact = tk.Entry(card, bg=COLOR_BG_DARK, fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID,
                                     insertbackground=COLOR_TEXT_LIGHT)
        self.form_contact.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        tk.Label(card, text="Status:", font=(FONT_FAMILY, 9, "bold"), fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY).grid(
            row=1, column=2, padx=6, pady=5, sticky=tk.W)
        self.form_status = ttk.Combobox(card, values=["Active", "Inactive", "Pending"], state="readonly", width=10)
        self.form_status.grid(row=1, column=3, padx=5, pady=5)

        btn_box = tk.Frame(card, bg=COLOR_SURFACE_NAVY)
        btn_box.grid(row=2, column=0, columnspan=6, pady=8, padx=5, sticky=tk.EW)

        tk.Button(btn_box, text="➕ Add Intake Record", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_PRIMARY_TEAL,
                  fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", width=18, command=self.add_record).pack(side=tk.LEFT,
                                                                                                     padx=3, ipady=4)
        tk.Button(btn_box, text="🔄 Toggle Priority", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_SURFACE_NAVY,
                  fg=COLOR_PRIMARY_TEAL, bd=1, relief=tk.SOLID, cursor="hand2", width=15,
                  command=self.toggle_priority).pack(side=tk.LEFT, padx=3, ipady=4)
        tk.Button(btn_box, text="🧹 Clear Fields", font=(FONT_FAMILY, 9, "bold"), bg="#475569", fg=COLOR_TEXT_LIGHT,
                  bd=0, cursor="hand2", width=12, command=self.clear_fields).pack(side=tk.LEFT, padx=3, ipady=4)
        tk.Button(btn_box, text="❌ Delete Patient", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_RED_DELETE,
                  fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", width=15, command=self.delete_record).pack(side=tk.RIGHT,
                                                                                                        padx=3, ipady=4)

        card.columnconfigure(1, weight=1)

    def build_right_panel(self):
        # Reporting Panel Anchor Card Controls
        lbl_head = tk.Label(self.right_panel, text="ANALYTICAL OPERATIONS", font=(FONT_FAMILY, 10, "bold"),
                            fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY)
        lbl_head.pack(fill=tk.X, ipady=8, pady=(0, 10))

        frame_viz = tk.LabelFrame(self.right_panel, text=" Dynamic Visualizations ", font=(FONT_FAMILY, 9, "bold"),
                                  fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID, padx=8, pady=8)
        frame_viz.pack(fill=tk.X, pady=(0, 10))

        tk.Button(frame_viz, text="📊 Launch Chart Analytics", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_PRIMARY_TEAL,
                  fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", command=self.launch_chart_window).pack(fill=tk.X, ipady=6,
                                                                                                    pady=5)

        frame_pdf = tk.LabelFrame(self.right_panel, text=" Export PDF Reports Engine ", font=(FONT_FAMILY, 9, "bold"),
                                  fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID, padx=8, pady=8)
        frame_pdf.pack(fill=tk.X)

        tk.Button(frame_pdf, text="📅 Generate Weekly Audit", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_SURFACE_NAVY,
                  fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID, cursor="hand2",
                  command=lambda: self.generate_text_pdf_report("Weekly")).pack(fill=tk.X, ipady=5, pady=4)
        tk.Button(frame_pdf, text="📅 Generate Monthly Audit", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_SURFACE_NAVY,
                  fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID, cursor="hand2",
                  command=lambda: self.generate_text_pdf_report("Monthly")).pack(fill=tk.X, ipady=5, pady=4)
        tk.Button(frame_pdf, text="📅 Generate Yearly Audit", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_SURFACE_NAVY,
                  fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID, cursor="hand2",
                  command=lambda: self.generate_text_pdf_report("Yearly")).pack(fill=tk.X, ipady=5, pady=4)

    def build_right_panel(self):
        self.right_panel.configure(bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID)

        lbl_head = tk.Label(self.right_panel, text="ANALYTICAL OPERATIONS", font=(FONT_FAMILY, 10, "bold"),
                            fg=COLOR_TEXT_LIGHT, bg=COLOR_SURFACE_NAVY)
        lbl_head.pack(fill=tk.X, ipady=8, pady=(0, 10))

        frame_viz = tk.LabelFrame(self.right_panel, text=" Dynamic Visualizations ", font=(FONT_FAMILY, 9, "bold"),
                                  fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID, padx=8, pady=8)
        frame_viz.pack(fill=tk.X, padx=10, pady=(0, 15))

        tk.Button(frame_viz, text="📊 Launch Chart Analytics", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_PRIMARY_TEAL,
                  fg=COLOR_TEXT_LIGHT, bd=0, cursor="hand2", command=self.launch_chart_window).pack(fill=tk.X, ipady=6,
                                                                                                    pady=5)

        frame_pdf = tk.LabelFrame(self.right_panel, text=" Export Reports Engine ", font=(FONT_FAMILY, 9, "bold"),
                                  fg=COLOR_PRIMARY_TEAL, bg=COLOR_SURFACE_NAVY, bd=1, relief=tk.SOLID, padx=8, pady=8)
        frame_pdf.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(frame_pdf, text="📅 Generate Weekly Audit", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_BG_DARK,
                  fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID, cursor="hand2",
                  command=lambda: self.generate_text_pdf_report("Weekly")).pack(fill=tk.X, ipady=5, pady=4)
        tk.Button(frame_pdf, text="📅 Generate Monthly Audit", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_BG_DARK,
                  fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID, cursor="hand2",
                  command=lambda: self.generate_text_pdf_report("Monthly")).pack(fill=tk.X, ipady=5, pady=4)
        tk.Button(frame_pdf, text="📅 Generate Yearly Audit", font=(FONT_FAMILY, 9, "bold"), bg=COLOR_BG_DARK,
                  fg=COLOR_TEXT_LIGHT, bd=1, relief=tk.SOLID, cursor="hand2",
                  command=lambda: self.generate_text_pdf_report("Yearly")).pack(fill=tk.X, ipady=5, pady=4)

        # Build it out
        self.right_panel.pack_propagate(False)

    # --- CORE REPO DATABASE LOGIC ENGINES ---
    def load_data_grid(self):
        """Fetches SQLite records dynamically based on active filtering terms."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        term = self.ent_search.get().strip()
        gender = self.cmb_gender.get()
        status = self.cmb_status.get()
        date_filter = self.cmb_date.get()

        query = "SELECT id, full_name, gender, age, created_date, status, contact_info, priority FROM records WHERE 1=1"
        params = []

        if term:
            query += " AND (id LIKE ? OR full_name LIKE ? OR status LIKE ?)"
            params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])

        if gender != "All":
            query += " AND gender = ?"
            params.append(gender)

        if status != "All":
            query += " AND status = ?"
            params.append(status)

        if date_filter != "All Dates":
            today = datetime.now().date()
            if "Daily" in date_filter:
                query += " AND created_date = ?"
                params.append(str(today))
            elif "Weekly" in date_filter:
                start_date = today - timedelta(days=7)
                query += " AND created_date >= ?"
                params.append(str(start_date))
            elif "Monthly" in date_filter:
                start_date = today - timedelta(days=30)
                query += " AND created_date >= ?"
                params.append(str(start_date))
            elif "Yearly" in date_filter:
                start_date = today - timedelta(days=365)
                query += " AND created_date >= ?"
                params.append(str(start_date))

        conn = sqlite3.connect("clinic_records.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def add_record(self):
        name = self.form_name.get().strip()
        gender = self.form_gender.get()
        age_str = self.form_age.get().strip()
        contact = self.form_contact.get().strip()
        status = self.form_status.get()

        if not (name and gender and age_str and contact and status):
            messagebox.showerror("Validation Error", "All fields must be completely filled out.")
            return

        try:
            age = int(age_str)
            if age < 0 or age > 120: raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Please input a valid numeric age parameter.")
            return

        # Standard structural optimization priority assessment logic
        priority = "Standard"
        if age <= 5 or age >= 60:
            priority = "High Priority (Triage)"

        today_str = str(datetime.now().date())

        conn = sqlite3.connect("clinic_records.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (full_name, gender, age, created_date, status, contact_info, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, gender, age, today_str, status, contact, priority))
        conn.commit()
        conn.close()

        self.load_data_grid()
        self.clear_fields()
        messagebox.showinfo("Success", "New dynamic patient intake track logged successfully.")

    def on_record_selected(self, event):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected[0], 'values')

        # Populate Form Entry Box controls quickly
        self.form_name.delete(0, tk.END)
        self.form_name.insert(0, values[1])
        self.form_gender.set(values[2])
        self.form_age.delete(0, tk.END)
        self.form_age.insert(0, values[3])
        self.form_contact.delete(0, tk.END)
        self.form_contact.insert(0, values[6])
        self.form_status.set(values[5])

    def toggle_priority(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   "Please choose a patient line row item from the grid table above to modify.")
            return
        record_id = self.tree.item(selected[0], 'values')[0]
        current_priority = self.tree.item(selected[0], 'values')[7]

        new_priority = "Standard" if current_priority != "Standard" else "High Priority (Triage)"

        conn = sqlite3.connect("clinic_records.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE records SET priority = ? WHERE id = ?", (new_priority, record_id))
        conn.commit()
        conn.close()

        self.load_data_grid()
        messagebox.showinfo("Modified", "Triage status classification state reversed.")

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a target row item entry to delete.")
            return
        record_id = self.tree.item(selected[0], 'values')[0]
        name = self.tree.item(selected[0], 'values')[1]

        if messagebox.askyesno("Confirm Purge",
                               f"Permanently discharge and remove '{name}' profile logs from tracking?"):
            conn = sqlite3.connect("clinic_records.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()

            self.load_data_grid()
            self.clear_fields()

    def clear_fields(self):
        self.form_name.delete(0, tk.END)
        self.form_gender.set('')
        self.form_age.delete(0, tk.END)
        self.form_contact.delete(0, tk.END)
        self.form_status.set('')

    # --- ADVANCED MATPLOTLIB ANALYTICS DASHBOARD ENGINE ---
    def launch_chart_window(self):
        """Dynamically tallies database states and spawns visual chart components."""
        conn = sqlite3.connect("clinic_records.db")
        cursor = conn.cursor()

        # Metric 1 Tally
        cursor.execute("SELECT status, COUNT(*) FROM records GROUP BY status")
        status_data = dict(cursor.fetchall())

        # Metric 2 Tally
        cursor.execute("SELECT gender, COUNT(*) FROM records GROUP BY gender")
        gender_data = dict(cursor.fetchall())

        # Metric 3 Tally
        cursor.execute(
            "SELECT created_date, COUNT(*) FROM records GROUP BY created_date ORDER BY created_date DESC LIMIT 7")
        trend_data = cursor.fetchall()
        trend_data.reverse()
        conn.close()

        # Safeguard fallback fills
        for k in ["Active", "Inactive", "Pending"]: status_data.setdefault(k, 0)
        for k in ["Male", "Female", "Other"]: gender_data.setdefault(k, 0)

        # Spawning window canvas components safely without crashes
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ImportError:
            messagebox.showerror("Library Missing",
                                 "Please install matplotlib in your execution terminal to launch analytics engine:\npip install matplotlib")
            return

        viz_win = tk.Toplevel(self)
        viz_win.title("Analytics Canvas Engine View Panel")
        viz_win.geometry("900x550")
        viz_win.configure(bg=COLOR_SURFACE_NAVY)

        # Styling configuration matching core dark aesthetics
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5), facecolor=COLOR_SURFACE_NAVY)

        # Bar Chart Logic Execution
        statuses = list(status_data.keys())
        counts = list(status_data.values())
        ax1.bar(statuses, counts, color=[COLOR_PRIMARY_TEAL, COLOR_GREEN_ACTIVE, COLOR_RED_DELETE])
        ax1.set_title("Volume by Status Group", color=COLOR_TEXT_LIGHT, fontname=FONT_FAMILY, fontsize=10,
                      weight="bold")
        ax1.set_facecolor(COLOR_BG_DARK)
        ax1.tick_params(colors=COLOR_TEXT_LIGHT)
        ax1.spines['bottom'].set_color(COLOR_TEXT_MUTED)
        ax1.spines['left'].set_color(COLOR_TEXT_MUTED)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        # Pie Chart Logic Execution
        genders = list(gender_data.keys())
        g_counts = list(gender_data.values())
        ax2.pie(g_counts, labels=genders, autopct='%1.1f%%', colors=['#38BDF8', '#F472B6', '#A78BFA'],
                textprops={'color': COLOR_TEXT_LIGHT})
        ax2.set_title("Gender Category Splits", color=COLOR_TEXT_LIGHT, fontname=FONT_FAMILY, fontsize=10,
                      weight="bold")

        # Line Chart Trend Logic Execution
        if trend_data:
            dates = [datetime.strptime(d[0], "%Y-%m-%d").strftime("%d-%b") for d in trend_data]
            t_counts = [d[1] for d in trend_data]
        else:
            dates, t_counts = ["None"], [0]

        ax3.plot(dates, t_counts, marker='o', color=COLOR_GREEN_ACTIVE, linewidth=2)
        ax3.set_title("Registration Trends", color=COLOR_TEXT_LIGHT, fontname=FONT_FAMILY, fontsize=10, weight="bold")
        ax3.set_facecolor(COLOR_BG_DARK)
        ax3.tick_params(colors=COLOR_TEXT_LIGHT)
        ax3.grid(True, color="#334155", linestyle="--")
        ax3.spines['bottom'].set_color(COLOR_TEXT_MUTED)
        ax3.spines['left'].set_color(COLOR_TEXT_MUTED)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=viz_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    # --- TEXT-BASED EXPORT AUDIT ENGINE (PDF SIMULATOR CONSOLE FORMAT) ---
    def generate_text_pdf_report(self, range_type):
        """Compiles clean statistical ledger reports targeting specified dates."""
        today = datetime.now().date()
        if range_type == "Weekly":
            start = today - timedelta(days=7)
        elif range_type == "Monthly":
            start = today - timedelta(days=30)
        else:
            start = today - timedelta(days=365)

        conn = sqlite3.connect("clinic_records.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, full_name, gender, age, created_date, status, priority 
            FROM records 
            WHERE created_date >= ? AND created_date <= ?
            ORDER BY created_date DESC
        """, (str(start), str(today)))
        rows = cursor.fetchall()

        # Metric Counts Summaries
        cursor.execute("SELECT status, COUNT(*) FROM records WHERE created_date >= ? GROUP BY status", (str(start),))
        summary_stats = dict(cursor.fetchall())
        conn.close()

        # File Stream Selection Dialog Box
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Official Document Audit Report Text", "*.txt"), ("All Files", "*.*")],
            title=f"Save Generated {range_type} Metric Summary Audit"
        )
        if not file_path: return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=" * 85 + "\n")
                f.write(f"           OFFICIAL HEALTH SERVICE AUDIT REPORT SUMMARY — {range_type.upper()}\n")
                f.write(f"           Supporting SDG 3 Infrastructure Targets & Medical Data Metrics\n")
                f.write("=" * 85 + "\n\n")
                f.write(f" Generated Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%M')}\n")
                f.write(f" Active Audit Window : {start} to {today}\n")
                f.write(f" Cumulative Records  : {len(rows)} Total Patients Registered inside this window frame.\n\n")

                f.write(" [SUMMARY STATISTICS MATRIX]\n")
                f.write(f"  • Active Status Volume   : {summary_stats.get('Active', 0)}\n")
                f.write(f"  • Pending Intake Volume  : {summary_stats.get('Pending', 0)}\n")
                f.write(f"  • Inactive Status Volume : {summary_stats.get('Inactive', 0)}\n\n")

                f.write(" [DETAILED MEDICAL PATIENT TRACKING REGISTRY TABLE]\n")
                f.write("-" * 90 + "\n")
                f.write(
                    f" {'ID':<4} | {'Patient Legal Name':<22} | {'Gender':<7} | {'Age':<4} | {'Created Date':<12} | {'Status':<8} | {'Priority':<15}\n")
                f.write("-" * 90 + "\n")

                for r in rows:
                    f.write(f" {r[0]:<4} | {r[1]:<22} | {r[2]:<7} | {r[3]:<4} | {r[4]:<12} | {r[5]:<8} | {r[6]:<15}\n")

                f.write("-" * 90 + "\n\n")
                f.write("=" * 85 + "\n")
                f.write(
                    " END OF AUDIT DOCUMENT LOG — CONFIDENTIAL HEALTH SERVICE DATA RECORDS PURGE PROTECTION ACTIVE\n")
                f.write("=" * 85 + "\n")

            messagebox.showinfo("Export Successful",
                                f"Your formatted text report was generated perfectly:\n{file_path}")
        except Exception as err:
            messagebox.showerror("System I/O Error", f"Failed to successfully stream data to disk: {str(err)}")


# --- PROGRAM ENVIRONMENT SYSTEM EXECUTION ANCHOR ---
if __name__ == "__main__":
    # Standard SQLite schema verification call
    initialize_database()

    # Run loop toolkit interface execution environment
    app = ApplicationToolkit()
    app.mainloop()