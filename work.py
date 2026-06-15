# ============================================================
#  PROG103 - PRINCIPLES OF STRUCTURED PROGRAMMING
#  Assignment 1: Student Record Management System (SRMS)
#  Interface : Tkinter GUI
#  SDG Goal  : SDG 4 - Quality Education
#  University: Limkokwing University - Sierra Leone
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
PASSING_GRADE = 50
MAX_SCORE     = 100
MIN_SCORE     = 0
SCHOOL_NAME   = "Limkokwing University – Sierra Leone"
APP_TITLE     = "Student Record Management System"

# ─────────────────────────────────────────────
#  COLOUR PALETTE  (dark theme)
# ─────────────────────────────────────────────
BG_DARK    = "#0d1117"
BG_PANEL   = "#161b22"
BG_CARD    = "#1c2128"
BG_INPUT   = "#21262d"
ACCENT     = "#00c896"
ACCENT2    = "#79c0ff"
TEXT_WHITE = "#e6edf3"
TEXT_MUTED = "#8b949e"
TEXT_GREEN = "#3fb950"
TEXT_RED   = "#ff7b72"
TEXT_AMBER = "#e3b341"
BORDER     = "#30363d"

SUBJECTS = ["Mathematics", "English", "Programming", "ICT"]

# ─────────────────────────────────────────────
#  DATA STORE
# ─────────────────────────────────────────────
students = []


# ============================================================
#  CORE LOGIC FUNCTIONS  (structured programming)
# ============================================================

def calculate_average(scores):
    """Returns the average of a list of scores."""
    if len(scores) == 0:
        return 0.0
    return sum(scores) / len(scores)


def assign_grade(average):
    """Returns a letter grade and remark based on average score."""
    if average >= 80:
        return "A", "Distinction"
    elif average >= 70:
        return "B", "Merit"
    elif average >= 60:
        return "C", "Credit"
    elif average >= 50:
        return "D", "Pass"
    else:
        return "F", "Fail"


def generate_student_id():
    """Auto-generates a unique student ID."""
    return f"STU{1000 + len(students) + 1}"


def get_grade_color(grade):
    """Returns a colour based on the grade letter."""
    if grade == "A":
        return ACCENT
    elif grade == "B":
        return TEXT_GREEN
    elif grade in ("C", "D"):
        return TEXT_AMBER
    else:
        return TEXT_RED


# ============================================================
#  REUSABLE UI HELPERS
# ============================================================

def make_label(parent, text, size=12, color=TEXT_WHITE, bold=False, anchor="w"):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, bg=parent["bg"],
                    fg=color, font=("Segoe UI", size, weight), anchor=anchor)


def make_entry(parent, textvariable=None, width=30):
    e = tk.Entry(parent, textvariable=textvariable, width=width,
                 bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=ACCENT,
                 relief="flat", font=("Segoe UI", 11),
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT)
    return e


def make_button(parent, text, command, color=ACCENT, fg=BG_DARK, width=18):
    return tk.Button(parent, text=text, command=command,
                     bg=color, fg=fg, font=("Segoe UI", 10, "bold"),
                     relief="flat", cursor="hand2", width=width,
                     activebackground=ACCENT2, activeforeground=BG_DARK,
                     padx=8, pady=6)


def card_frame(parent, padx=16, pady=12):
    f = tk.Frame(parent, bg=BG_CARD,
                 highlightthickness=1, highlightbackground=BORDER)
    f.pack(fill="x", padx=padx, pady=pady)
    return f


# ============================================================
#  MAIN APPLICATION CLASS
# ============================================================

class SRMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} — {SCHOOL_NAME}")
        self.root.geometry("1100x720")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG_DARK)

        self._build_sidebar()
        self._build_main_area()
        self._show_dashboard()

    # ── SIDEBAR ─────────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=BG_PANEL, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo / title area
        logo_frame = tk.Frame(self.sidebar, bg=ACCENT, height=70)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        tk.Label(logo_frame, text="SRMS", bg=ACCENT, fg=BG_DARK,
                 font=("Segoe UI", 22, "bold")).pack(expand=True)

        tk.Label(self.sidebar, text=SCHOOL_NAME, bg=BG_PANEL,
                 fg=TEXT_MUTED, font=("Segoe UI", 8),
                 wraplength=200, justify="center").pack(pady=(10, 20))

        # Nav buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠  Dashboard",   self._show_dashboard),
            ("➕  Add Student",  self._show_add_student),
            ("📋  All Records",  self._show_all_records),
            ("🔍  Search",       self._show_search),
            ("📊  Class Report", self._show_class_report),
            ("🏆  Top Student",  self._show_top_student),
            ("🗑   Delete Record", self._show_delete),
        ]
        for label, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=label, command=cmd,
                            bg=BG_PANEL, fg=TEXT_WHITE,
                            font=("Segoe UI", 10), relief="flat",
                            anchor="w", padx=20, pady=10, cursor="hand2",
                            activebackground=BG_CARD, activeforeground=ACCENT,
                            width=22)
            btn.pack(fill="x")
            self.nav_buttons[label] = btn

        # Footer
        tk.Label(self.sidebar, text="PROG103 · Semester 02 · 2026",
                 bg=BG_PANEL, fg=TEXT_MUTED,
                 font=("Segoe UI", 8)).pack(side="bottom", pady=12)

    def _set_active_nav(self, active_label):
        for label, btn in self.nav_buttons.items():
            if label == active_label:
                btn.config(bg=BG_CARD, fg=ACCENT)
            else:
                btn.config(bg=BG_PANEL, fg=TEXT_WHITE)

    # ── MAIN CONTENT AREA ───────────────────────────────────
    def _build_main_area(self):
        self.main = tk.Frame(self.root, bg=BG_DARK)
        self.main.pack(side="left", fill="both", expand=True)

    def _clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def _page_header(self, title, subtitle=""):
        header = tk.Frame(self.main, bg=BG_DARK)
        header.pack(fill="x", padx=24, pady=(20, 4))
        tk.Label(header, text=title, bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(header, text=subtitle, bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Segoe UI", 10)).pack(anchor="w")
        tk.Frame(self.main, bg=BORDER, height=1).pack(fill="x", padx=24, pady=6)

    # ── DASHBOARD ───────────────────────────────────────────
    def _show_dashboard(self):
        self._clear_main()
        self._set_active_nav("🏠  Dashboard")
        self._page_header("Dashboard", "Welcome to the Student Record Management System")

        # Stat cards row
        stats_frame = tk.Frame(self.main, bg=BG_DARK)
        stats_frame.pack(fill="x", padx=24, pady=10)

        total     = len(students)
        passing   = sum(1 for s in students if s["remark"] != "Fail")
        failing   = total - passing
        avg_score = round(calculate_average([s["average"] for s in students]), 2) if students else 0.0

        stats = [
            ("Total Students", str(total),   ACCENT2),
            ("Passing",        str(passing),  TEXT_GREEN),
            ("Failing",        str(failing),  TEXT_RED),
            ("Class Average",  f"{avg_score}%", TEXT_AMBER),
        ]
        for label, value, color in stats:
            card = tk.Frame(stats_frame, bg=BG_CARD,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(side="left", expand=True, fill="both", padx=6, pady=4)
            tk.Label(card, text=value, bg=BG_CARD, fg=color,
                     font=("Segoe UI", 28, "bold")).pack(pady=(14, 2))
            tk.Label(card, text=label, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Segoe UI", 10)).pack(pady=(0, 14))

        # Recent records
        tk.Label(self.main, text="Recent Records", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=24, pady=(16, 6))

        if not students:
            tk.Label(self.main,
                     text="No records yet. Use 'Add Student' to get started.",
                     bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Segoe UI", 11)).pack(padx=24, pady=30)
        else:
            self._build_table(self.main, students[-5:][::-1])

    # ── ADD STUDENT ─────────────────────────────────────────
    def _show_add_student(self):
        self._clear_main()
        self._set_active_nav("➕  Add Student")
        self._page_header("Add New Student", "Fill in the details below to register a student")

        scroll_canvas = tk.Canvas(self.main, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main, orient="vertical",
                                   command=scroll_canvas.yview)
        scroll_frame = tk.Frame(scroll_canvas, bg=BG_DARK)
        scroll_frame.bind("<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        form = card_frame(scroll_frame, padx=24, pady=10)

        # Basic info
        tk.Label(form, text="Student Information", bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 11, "bold")).grid(
                     row=0, column=0, columnspan=4, sticky="w", padx=16, pady=(12, 8))

        self.var_name      = tk.StringVar()
        self.var_age       = tk.StringVar()
        self.var_programme = tk.StringVar()

        fields = [
            ("Full Name",      self.var_name,      1, 0),
            ("Age",            self.var_age,        1, 2),
            ("Programme",      self.var_programme,  2, 0),
        ]
        for label, var, row, col in fields:
            tk.Label(form, text=label, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Segoe UI", 10)).grid(
                         row=row, column=col, sticky="w", padx=(16, 4), pady=6)
            make_entry(form, textvariable=var, width=26).grid(
                row=row, column=col+1, sticky="ew", padx=(0, 16), pady=6)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        # Subject scores
        sep = tk.Frame(form, bg=BORDER, height=1)
        sep.grid(row=3, column=0, columnspan=4, sticky="ew", padx=16, pady=8)
        tk.Label(form, text="Subject Scores  (0 – 100)", bg=BG_CARD,
                 fg=ACCENT, font=("Segoe UI", 11, "bold")).grid(
                     row=4, column=0, columnspan=4, sticky="w", padx=16, pady=(0, 8))

        self.score_vars = {}
        for idx, subject in enumerate(SUBJECTS):
            row_n = 5 + idx // 2
            col_n = (idx % 2) * 2
            tk.Label(form, text=subject, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Segoe UI", 10)).grid(
                         row=row_n, column=col_n, sticky="w", padx=(16, 4), pady=6)
            var = tk.StringVar()
            make_entry(form, textvariable=var, width=10).grid(
                row=row_n, column=col_n+1, sticky="ew", padx=(0, 16), pady=6)
            self.score_vars[subject] = var

        # Buttons
        btn_frame = tk.Frame(form, bg=BG_CARD)
        btn_frame.grid(row=9, column=0, columnspan=4, pady=16, padx=16, sticky="e")
        make_button(btn_frame, "Clear Form", self._clear_add_form,
                    color=BG_INPUT, fg=TEXT_WHITE).pack(side="left", padx=(0, 8))
        make_button(btn_frame, "Save Record ✓", self._save_student).pack(side="left")

        # Result label
        self.add_result_label = tk.Label(scroll_frame, text="", bg=BG_DARK,
                                          font=("Segoe UI", 11))
        self.add_result_label.pack(padx=24, pady=8, anchor="w")

    def _clear_add_form(self):
        self.var_name.set("")
        self.var_age.set("")
        self.var_programme.set("")
        for var in self.score_vars.values():
            var.set("")
        self.add_result_label.config(text="")

    def _save_student(self):
        # Validate name
        name = self.var_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Student name cannot be empty.")
            return

        # Validate age
        try:
            age = int(self.var_age.get().strip())
            if age <= 0 or age > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age (1–100).")
            return

        programme = self.var_programme.get().strip() or "Not Specified"

        # Validate scores
        scores = []
        for subject in SUBJECTS:
            raw = self.score_vars[subject].get().strip()
            try:
                score = float(raw)
                if not (MIN_SCORE <= score <= MAX_SCORE):
                    raise ValueError
                scores.append(score)
            except ValueError:
                messagebox.showerror("Error",
                    f"Invalid score for {subject}.\nEnter a number between 0 and 100.")
                return

        # Process
        average         = calculate_average(scores)
        grade, remark   = assign_grade(average)
        passed_subjects = sum(1 for s in scores if s >= PASSING_GRADE)
        failed_subjects = len(SUBJECTS) - passed_subjects
        student_id      = generate_student_id()

        record = {
            "id"              : student_id,
            "name"            : name,
            "age"             : age,
            "programme"       : programme,
            "subjects"        : SUBJECTS,
            "scores"          : scores,
            "average"         : round(average, 2),
            "grade"           : grade,
            "remark"          : remark,
            "passed_subjects" : passed_subjects,
            "failed_subjects" : failed_subjects,
        }
        students.append(record)

        color = get_grade_color(grade)
        self.add_result_label.config(
            text=f"✓  Saved!  ID: {student_id}   Average: {average:.2f}%   "
                 f"Grade: {grade}   {remark}",
            fg=color)
        self._clear_add_form()
        messagebox.showinfo("Success",
            f"Student '{name}' added successfully!\n"
            f"ID: {student_id} | Average: {average:.2f}% | Grade: {grade} ({remark})")

    # ── ALL RECORDS ─────────────────────────────────────────
    def _show_all_records(self):
        self._clear_main()
        self._set_active_nav("📋  All Records")
        self._page_header("All Student Records",
                          f"{len(students)} record(s) in the system")

        if not students:
            tk.Label(self.main,
                     text="No records found. Add a student first.",
                     bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Segoe UI", 12)).pack(pady=40)
            return

        self._build_table(self.main, students)

    def _build_table(self, parent, data):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=BG_CARD, foreground=TEXT_WHITE,
                        fieldbackground=BG_CARD, rowheight=32,
                        font=("Segoe UI", 10))
        style.configure("Dark.Treeview.Heading",
                        background=BG_PANEL, foreground=ACCENT,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", "#1f6feb")],
                  foreground=[("selected", TEXT_WHITE)])

        cols = ("ID", "Name", "Age", "Programme", "Average", "Grade", "Remark")
        frame = tk.Frame(parent, bg=BG_DARK)
        frame.pack(fill="both", expand=True, padx=24, pady=8)

        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="Dark.Treeview", height=16)

        widths = [80, 180, 50, 170, 80, 60, 100]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center" if col not in ("Name", "Programme") else "w")

        for rec in data:
            color_tag = rec["grade"]
            tree.insert("", "end", values=(
                rec["id"], rec["name"], rec["age"], rec["programme"],
                f"{rec['average']}%", rec["grade"], rec["remark"]
            ), tags=(color_tag,))

        tree.tag_configure("A", foreground=ACCENT)
        tree.tag_configure("B", foreground=TEXT_GREEN)
        tree.tag_configure("C", foreground=TEXT_AMBER)
        tree.tag_configure("D", foreground=TEXT_AMBER)
        tree.tag_configure("F", foreground=TEXT_RED)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    # ── SEARCH ──────────────────────────────────────────────
    def _show_search(self):
        self._clear_main()
        self._set_active_nav("🔍  Search")
        self._page_header("Search Student", "Search by name or student ID")

        search_frame = tk.Frame(self.main, bg=BG_DARK)
        search_frame.pack(fill="x", padx=24, pady=10)

        self.search_var = tk.StringVar()
        entry = make_entry(search_frame, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=(0, 10), ipady=4)
        entry.bind("<Return>", lambda e: self._do_search())
        make_button(search_frame, "Search 🔍", self._do_search, width=12).pack(side="left")

        self.search_result_frame = tk.Frame(self.main, bg=BG_DARK)
        self.search_result_frame.pack(fill="both", expand=True)

    def _do_search(self):
        for w in self.search_result_frame.winfo_children():
            w.destroy()

        keyword = self.search_var.get().strip().lower()
        if not keyword:
            tk.Label(self.search_result_frame, text="Please enter a search term.",
                     bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Segoe UI", 11)).pack(pady=20)
            return

        results = [r for r in students
                   if keyword in r["name"].lower() or keyword in r["id"].lower()]

        if not results:
            tk.Label(self.search_result_frame,
                     text=f"No student found matching '{keyword}'.",
                     bg=BG_DARK, fg=TEXT_RED,
                     font=("Segoe UI", 11)).pack(pady=20)
            return

        tk.Label(self.search_result_frame,
                 text=f"Found {len(results)} record(s):",
                 bg=BG_DARK, fg=TEXT_GREEN,
                 font=("Segoe UI", 11)).pack(anchor="w", padx=24, pady=(8, 4))

        for rec in results:
            self._student_detail_card(self.search_result_frame, rec)

    # ── CLASS REPORT ────────────────────────────────────────
    def _show_class_report(self):
        self._clear_main()
        self._set_active_nav("📊  Class Report")
        self._page_header("Class Average Report", "Overall performance summary")

        if not students:
            tk.Label(self.main, text="No records available.",
                     bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Segoe UI", 12)).pack(pady=40)
            return

        all_avgs      = [s["average"] for s in students]
        total_avg     = round(calculate_average(all_avgs), 2)
        grade, remark = assign_grade(total_avg)
        pass_count    = sum(1 for s in students if s["remark"] != "Fail")
        fail_count    = len(students) - pass_count

        stats = [
            ("Total Students",   str(len(students)), TEXT_WHITE),
            ("Class Average",    f"{total_avg}%",    get_grade_color(grade)),
            ("Class Grade",      f"{grade} – {remark}", get_grade_color(grade)),
            ("Passing Students", str(pass_count),    TEXT_GREEN),
            ("Failing Students", str(fail_count),    TEXT_RED),
        ]

        for label, value, color in stats:
            row = tk.Frame(self.main, bg=BG_CARD,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", padx=24, pady=4)
            tk.Label(row, text=label, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Segoe UI", 11), width=22, anchor="w").pack(
                         side="left", padx=16, pady=12)
            tk.Label(row, text=value, bg=BG_CARD, fg=color,
                     font=("Segoe UI", 13, "bold")).pack(side="left")

        # Subject averages
        tk.Label(self.main, text="Average Score Per Subject",
                 bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Segoe UI", 13, "bold")).pack(
                     anchor="w", padx=24, pady=(20, 6))

        for i, subject in enumerate(SUBJECTS):
            sub_avg = round(calculate_average([s["scores"][i] for s in students]), 2)
            sub_grade, _ = assign_grade(sub_avg)
            bar_frame = tk.Frame(self.main, bg=BG_CARD,
                                 highlightthickness=1, highlightbackground=BORDER)
            bar_frame.pack(fill="x", padx=24, pady=3)
            tk.Label(bar_frame, text=subject, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Segoe UI", 10), width=16, anchor="w").pack(
                         side="left", padx=16, pady=10)
            tk.Label(bar_frame, text=f"{sub_avg}%", bg=BG_CARD,
                     fg=get_grade_color(sub_grade),
                     font=("Segoe UI", 11, "bold")).pack(side="left")

    # ── TOP STUDENT ─────────────────────────────────────────
    def _show_top_student(self):
        self._clear_main()
        self._set_active_nav("🏆  Top Student")
        self._page_header("Top Performing Student", "Highest average score in the class")

        if not students:
            tk.Label(self.main, text="No records available.",
                     bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Segoe UI", 12)).pack(pady=40)
            return

        best = students[0]
        for rec in students:
            if rec["average"] > best["average"]:
                best = rec

        trophy = tk.Label(self.main, text="🏆", bg=BG_DARK,
                          font=("Segoe UI", 48))
        trophy.pack(pady=(20, 4))
        tk.Label(self.main, text=best["name"], bg=BG_DARK, fg=ACCENT,
                 font=("Segoe UI", 20, "bold")).pack()
        tk.Label(self.main, text=f"Average: {best['average']}%  |  Grade: {best['grade']}  |  {best['remark']}",
                 bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Segoe UI", 11)).pack(pady=(2, 16))

        self._student_detail_card(self.main, best)

    # ── DELETE ──────────────────────────────────────────────
    def _show_delete(self):
        self._clear_main()
        self._set_active_nav("🗑   Delete Record")
        self._page_header("Delete Student Record", "Remove a student by ID")

        frame = card_frame(self.main, padx=24, pady=12)
        tk.Label(frame, text="Enter Student ID", bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=16, pady=(12, 4))

        self.del_var = tk.StringVar()
        make_entry(frame, textvariable=self.del_var, width=20).pack(
            anchor="w", padx=16, pady=(0, 12))
        make_button(frame, "Delete Student", self._do_delete,
                    color=TEXT_RED, fg=TEXT_WHITE, width=16).pack(
                        anchor="w", padx=16, pady=(0, 14))

        self.del_status = tk.Label(self.main, text="", bg=BG_DARK,
                                   font=("Segoe UI", 11))
        self.del_status.pack(anchor="w", padx=24, pady=8)

    def _do_delete(self):
        sid = self.del_var.get().strip().upper()
        if not sid:
            messagebox.showerror("Error", "Please enter a Student ID.")
            return

        target = next((s for s in students if s["id"] == sid), None)
        if target is None:
            self.del_status.config(text=f"No student found with ID '{sid}'.",
                                   fg=TEXT_RED)
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{target['name']}' (ID: {sid})?")
        if confirm:
            students.remove(target)
            self.del_status.config(
                text=f"✓  '{target['name']}' has been deleted successfully.",
                fg=TEXT_GREEN)
            self.del_var.set("")

    # ── STUDENT DETAIL CARD ─────────────────────────────────
    def _student_detail_card(self, parent, rec):
        card = tk.Frame(parent, bg=BG_CARD,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", padx=24, pady=8)

        # Header row
        head = tk.Frame(card, bg=BG_PANEL)
        head.pack(fill="x")
        tk.Label(head, text=rec["id"], bg=BG_PANEL, fg=ACCENT2,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=16, pady=10)
        tk.Label(head, text=rec["name"], bg=BG_PANEL, fg=TEXT_WHITE,
                 font=("Segoe UI", 12, "bold")).pack(side="left")
        grade_color = get_grade_color(rec["grade"])
        tk.Label(head,
                 text=f"  {rec['grade']} – {rec['remark']}  ",
                 bg=BG_PANEL, fg=grade_color,
                 font=("Segoe UI", 10, "bold")).pack(side="right", padx=16)

        # Info row
        info = tk.Frame(card, bg=BG_CARD)
        info.pack(fill="x", padx=16, pady=(8, 4))
        for label, val in [("Age", rec["age"]), ("Programme", rec["programme"]),
                           ("Average", f"{rec['average']}%")]:
            tk.Label(info, text=f"{label}: ", bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Segoe UI", 10)).pack(side="left")
            tk.Label(info, text=str(val), bg=BG_CARD, fg=TEXT_WHITE,
                     font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 20))

        # Subject scores row
        scores_row = tk.Frame(card, bg=BG_CARD)
        scores_row.pack(fill="x", padx=16, pady=(4, 12))
        for i, subject in enumerate(rec["subjects"]):
            score  = rec["scores"][i]
            status = "PASS" if score >= PASSING_GRADE else "FAIL"
            color  = TEXT_GREEN if status == "PASS" else TEXT_RED
            box = tk.Frame(scores_row, bg=BG_INPUT,
                           highlightthickness=1, highlightbackground=BORDER)
            box.pack(side="left", padx=(0, 8), pady=2, ipadx=6, ipady=4)
            tk.Label(box, text=subject, bg=BG_INPUT, fg=TEXT_MUTED,
                     font=("Segoe UI", 9)).pack()
            tk.Label(box, text=f"{score:.1f}", bg=BG_INPUT, fg=TEXT_WHITE,
                     font=("Segoe UI", 12, "bold")).pack()
            tk.Label(box, text=status, bg=BG_INPUT, fg=color,
                     font=("Segoe UI", 8, "bold")).pack()


# ============================================================
#  ENTRY POINT
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app  = SRMSApp(root)
    root.mainloop()