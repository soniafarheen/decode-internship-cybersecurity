"""
Password Security Dashboard
Password Security Dashboard - Project 1 (Cyber Security Track)

A modern, multi-section desktop dashboard built entirely in Python (Tkinter).

Sections:
  1. Strength Checker - analyze a password and see a live breakdown
  2. Password Generator - create strong random passwords with custom rules
  3. Security Tips - best-practice guidance
  4. History - session log of checked/generated passwords

Key Skills demonstrated: string handling, conditional logic, security basics,
GUI/dashboard design, randomization.
"""

import tkinter as tk
from tkinter import ttk
import string
import random
import datetime
import os

# ---------------------------------------------------------------------------
# THEME / COLORS -- Kali Purple inspired (dark, purple/blue gradient)
# ---------------------------------------------------------------------------
BG_SIDEBAR = "#0d0b1a"
BG_MAIN = "#0c0a16"
BG_CARD = "#161329"
ACCENT = "#8b5cf6"        # Kali Purple accent
ACCENT_BLUE = "#367bf0"   # Kali dragon blue
ACCENT_SOFT = "#251f45"
GRADIENT_TOP = "#2a1a5e"
GRADIENT_BOTTOM = "#12102a"
TEXT_MAIN = "#ece9fb"
TEXT_MUTED = "#78708f"
WEAK_COLOR = "#ff4c4c"
MED_COLOR = "#ffb100"
STRONG_COLOR = "#00e08a"

FONT_TITLE = ("Consolas", 20, "bold")
FONT_SUB = ("Consolas", 10)
FONT_H2 = ("Consolas", 14, "bold")
FONT_BODY = ("Consolas", 11)
FONT_SMALL = ("Consolas", 9)
FONT_MONO = ("Consolas", 14, "bold")

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "111111", "12345678", "iloveyou", "admin",
    "letmein", "welcome", "monkey", "dragon", "football"
}
SYMBOLS = string.punctuation


# ---------------------------------------------------------------------------
# CORE LOGIC
# ---------------------------------------------------------------------------
def check_password_strength(password: str) -> dict:
    length = len(password)

    if password.lower() in COMMON_PASSWORDS:
        return {
            "length": length, "has_upper": False, "has_lower": False,
            "has_digit": False, "has_symbol": False, "is_common": True,
            "score": 0, "strength": "Weak",
            "feedback": ["This password is in a common/leaked password list."],
        }

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in SYMBOLS for c in password)

    feedback = []
    score = 0

    if length >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")
    if length >= 12:
        score += 1
    if has_upper and has_lower:
        score += 1
    else:
        feedback.append("Mix uppercase and lowercase letters.")
    if has_digit:
        score += 1
    else:
        feedback.append("Add at least one number.")
    if has_symbol:
        score += 1
    else:
        feedback.append("Add at least one symbol (e.g. ! @ # $).")

    if length < 8:
        strength = "Weak"
    elif score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "length": length, "has_upper": has_upper, "has_lower": has_lower,
        "has_digit": has_digit, "has_symbol": has_symbol, "is_common": False,
        "score": score, "strength": strength, "feedback": feedback,
    }


def generate_password(length=14, use_upper=True, use_lower=True,
                       use_digits=True, use_symbols=True) -> str:
    pool = ""
    required = []

    if use_upper:
        pool += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))
    if use_lower:
        pool += string.ascii_lowercase
        required.append(random.choice(string.ascii_lowercase))
    if use_digits:
        pool += string.digits
        required.append(random.choice(string.digits))
    if use_symbols:
        pool += string.punctuation
        required.append(random.choice(string.punctuation))

    if not pool:
        pool = string.ascii_lowercase
        required = [random.choice(string.ascii_lowercase)]

    remaining = max(length - len(required), 0)
    body = [random.choice(pool) for _ in range(remaining)]
    result = required + body
    random.shuffle(result)
    return "".join(result)[:max(length, len(required))]


STRENGTH_COLORS = {"Weak": WEAK_COLOR, "Medium": MED_COLOR, "Strong": STRONG_COLOR}


# ---------------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------------
class PasswordDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔒 Password Security Dashboard")
        self.geometry("980x640")
        self.minsize(900, 600)
        self.configure(bg=BG_MAIN)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.history = []  # list of dicts: {time, source, value_masked, strength}

        self._build_sidebar()
        self._build_content_area()

        self.frames = {}
        self._build_checker_frame()
        self._build_generator_frame()
        self._build_tips_frame()
        self._build_history_frame()

        self.show_frame("checker")

    def _draw_gradient(self, canvas, width, height, color1, color2):
        """Paint a smooth vertical gradient onto a Canvas."""
        r1, g1, b1 = [c // 256 for c in canvas.winfo_rgb(color1)]
        r2, g2, b2 = [c // 256 for c in canvas.winfo_rgb(color2)]
        for i in range(height):
            t = i / max(height - 1, 1)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            canvas.create_line(0, i, width, i, fill=f"#{r:02x}{g:02x}{b:02x}")

    # ---------------- SIDEBAR ----------------
    def _build_sidebar(self):
        sidebar = tk.Frame(self, bg=BG_SIDEBAR, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # --- Gradient header panel (Kali Purple style) ---
        header_h = 170
        header_canvas = tk.Canvas(sidebar, width=220, height=header_h,
                                   highlightthickness=0, bd=0)
        header_canvas.pack(fill="x")
        self._draw_gradient(header_canvas, 220, header_h, GRADIENT_TOP, GRADIENT_BOTTOM)

        # Lock icon (loaded once, kept as attribute to avoid garbage collection)
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        self.logo_img = None
        if os.path.exists(icon_path):
            try:
                raw = tk.PhotoImage(file=icon_path)
                self.logo_img = raw.subsample(4, 4)  # 256px -> ~64px
            except Exception:
                self.logo_img = None

        if self.logo_img:
            header_canvas.create_image(110, 58, image=self.logo_img)
        else:
            header_canvas.create_text(110, 55, text="🔒", font=("Segoe UI", 30),
                                       fill="#ffffff")

        header_canvas.create_text(110, 118, text="SecureCheck",
                                   font=("Segoe UI", 15, "bold"), fill="#ffffff")
        header_canvas.create_text(110, 140, text="Security Dashboard",
                                   font=FONT_SMALL, fill="#d8d3ff")

        tk.Frame(sidebar, bg=BG_SIDEBAR, height=16).pack(fill="x")

        self.nav_buttons = {}
        nav_items = [
            ("checker", "🔒  Strength Checker"),
            ("generator", "🔑  Password Generator"),
            ("tips", "💡  Security Tips"),
            ("history", "📊  History"),
        ]
        for key, label in nav_items:
            btn = tk.Label(
                sidebar, text=label, font=FONT_BODY, bg=BG_SIDEBAR,
                fg=TEXT_MUTED, anchor="w", padx=24, pady=12, cursor="hand2"
            )
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, k=key: self.show_frame(k))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=ACCENT_SOFT, fg=TEXT_MAIN))
            btn.bind("<Leave>", lambda e, b=btn, k=key: self._unhover(b, k))
            self.nav_buttons[key] = btn

        tk.Label(sidebar, text="Runs 100% locally.\nNo data leaves this app.",
                 font=FONT_SMALL, bg=BG_SIDEBAR, fg=TEXT_MUTED,
                 justify="left").pack(side="bottom", pady=20, padx=24, anchor="w")

    def _unhover(self, btn, key):
        if self.current_frame_key != key:
            btn.config(bg=BG_SIDEBAR, fg=TEXT_MUTED)

    def show_frame(self, key):
        self.current_frame_key = key
        for k, f in self.frames.items():
            f.pack_forget()
        for k, b in self.nav_buttons.items():
            if k == key:
                b.config(bg=ACCENT_SOFT, fg=TEXT_MAIN)
            else:
                b.config(bg=BG_SIDEBAR, fg=TEXT_MUTED)
        self.frames[key].pack(fill="both", expand=True, padx=30, pady=26)
        if key == "history":
            self._refresh_history_view()

    # ---------------- CONTENT AREA ----------------
    def _build_content_area(self):
        self.content = tk.Frame(self, bg=BG_MAIN)
        self.content.pack(side="left", fill="both", expand=True)

    def _card(self, parent, **kwargs):
        f = tk.Frame(parent, bg=BG_CARD, **kwargs)
        return f

    # ---------------- CHECKER FRAME ----------------
    def _build_checker_frame(self):
        frame = tk.Frame(self.content, bg=BG_MAIN)
        self.frames["checker"] = frame

        tk.Label(frame, text="Password Strength Checker", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_MAIN).pack(anchor="w")
        tk.Label(frame, text="Type a password to see a full security breakdown.",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        card = self._card(frame)
        card.pack(fill="x")
        inner = tk.Frame(card, bg=BG_CARD, padx=24, pady=24)
        inner.pack(fill="x")

        entry_row = tk.Frame(inner, bg=BG_CARD)
        entry_row.pack(fill="x")

        self.pwd_var = tk.StringVar()
        self.show_var = tk.BooleanVar(value=False)

        self.pwd_entry = tk.Entry(
            entry_row, textvariable=self.pwd_var, font=FONT_MONO, show="•",
            bg="#242b45", fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
            relief="flat", bd=0
        )
        self.pwd_entry.pack(side="left", fill="x", expand=True, ipady=10, ipadx=10)
        self.pwd_entry.bind("<KeyRelease>", lambda e: self._update_checker())

        show_chk = tk.Checkbutton(
            entry_row, text="Show", variable=self.show_var, bg=BG_CARD,
            fg=TEXT_MUTED, selectcolor=BG_CARD, activebackground=BG_CARD,
            font=FONT_SMALL, command=self._toggle_show
        )
        show_chk.pack(side="left", padx=(12, 0))

        save_btn = tk.Label(entry_row, text="Save to History", bg=ACCENT,
                             fg="#ffffff", font=FONT_SMALL, padx=14, pady=8,
                             cursor="hand2")
        save_btn.pack(side="left", padx=(12, 0))
        save_btn.bind("<Button-1>", lambda e: self._save_checker_to_history())

        # strength bar
        self.bar_canvas = tk.Canvas(inner, height=12, bg="#242b45",
                                     highlightthickness=0)
        self.bar_canvas.pack(fill="x", pady=(20, 6))
        self.bar_fill = self.bar_canvas.create_rectangle(0, 0, 0, 12, width=0)

        self.result_label = tk.Label(inner, text="Start typing a password...",
                                      font=FONT_H2, bg=BG_CARD, fg=TEXT_MUTED)
        self.result_label.pack(anchor="w", pady=(4, 16))

        # checklist + feedback side by side
        cols = tk.Frame(inner, bg=BG_CARD)
        cols.pack(fill="x")

        checklist_col = tk.Frame(cols, bg=BG_CARD)
        checklist_col.pack(side="left", fill="both", expand=True, anchor="n")
        tk.Label(checklist_col, text="CRITERIA", font=("Segoe UI", 9, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 8))

        self.check_items = {}
        labels_text = {
            "len": "At least 8 characters",
            "upper_lower": "Mixed upper & lowercase",
            "digit": "Contains a number",
            "symbol": "Contains a symbol",
            "common": "Not a common/leaked password",
        }
        for key, text in labels_text.items():
            lbl = tk.Label(checklist_col, text="○  " + text, font=FONT_BODY,
                            bg=BG_CARD, fg=TEXT_MUTED, anchor="w")
            lbl.pack(fill="x", pady=3)
            self.check_items[key] = (lbl, text)

        feedback_col = tk.Frame(cols, bg=BG_CARD)
        feedback_col.pack(side="left", fill="both", expand=True, anchor="n", padx=(30, 0))
        tk.Label(feedback_col, text="SUGGESTIONS", font=("Segoe UI", 9, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 8))
        self.feedback_label = tk.Label(feedback_col, text="—", font=FONT_BODY,
                                        bg=BG_CARD, fg=TEXT_MUTED, anchor="w",
                                        justify="left", wraplength=320)
        self.feedback_label.pack(fill="x")

    def _toggle_show(self):
        self.pwd_entry.config(show="" if self.show_var.get() else "•")

    def _update_checker(self):
        pwd = self.pwd_var.get()
        if not pwd:
            self.bar_canvas.coords(self.bar_fill, 0, 0, 0, 12)
            self.result_label.config(text="Start typing a password...", fg=TEXT_MUTED)
            for key, (lbl, text) in self.check_items.items():
                lbl.config(text="○  " + text, fg=TEXT_MUTED)
            self.feedback_label.config(text="—")
            return

        report = check_password_strength(pwd)

        def set_item(key, passed):
            lbl, text = self.check_items[key]
            mark = "●" if passed else "○"
            color = STRONG_COLOR if passed else TEXT_MUTED
            lbl.config(text=f"{mark}  {text}", fg=color)

        set_item("len", report["length"] >= 8)
        set_item("upper_lower", report["has_upper"] and report["has_lower"])
        set_item("digit", report["has_digit"])
        set_item("symbol", report["has_symbol"])
        set_item("common", not report["is_common"])

        strength = report["strength"]
        color = STRENGTH_COLORS[strength]
        canvas_w = self.bar_canvas.winfo_width() or 600
        pct = {"Weak": 0.25, "Medium": 0.65, "Strong": 1.0}[strength]
        self.bar_canvas.coords(self.bar_fill, 0, 0, canvas_w * pct, 12)
        self.bar_canvas.itemconfig(self.bar_fill, fill=color)
        self.result_label.config(text=f"Strength: {strength}", fg=color)

        fb = report.get("feedback", [])
        self.feedback_label.config(text="\n".join("• " + f for f in fb) if fb
                                    else "✓ Looks great — no issues found.")

        self._last_checker_report = report
        self._last_checker_pwd = pwd

    def _save_checker_to_history(self):
        pwd = self.pwd_var.get()
        if not pwd:
            return
        report = check_password_strength(pwd)
        self._add_history("Checked", pwd, report["strength"])

    # ---------------- GENERATOR FRAME ----------------
    def _build_generator_frame(self):
        frame = tk.Frame(self.content, bg=BG_MAIN)
        self.frames["generator"] = frame

        tk.Label(frame, text="Password Generator", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_MAIN).pack(anchor="w")
        tk.Label(frame, text="Create a strong random password with custom rules.",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        card = self._card(frame)
        card.pack(fill="x")
        inner = tk.Frame(card, bg=BG_CARD, padx=24, pady=24)
        inner.pack(fill="x")

        # generated password display
        display_row = tk.Frame(inner, bg="#242b45")
        display_row.pack(fill="x")
        self.gen_pwd_var = tk.StringVar(value="Click Generate to create a password")
        gen_label = tk.Label(display_row, textvariable=self.gen_pwd_var, font=FONT_MONO,
                              bg="#242b45", fg=TEXT_MAIN, anchor="w", padx=14, pady=14)
        gen_label.pack(side="left", fill="x", expand=True)

        copy_btn = tk.Label(display_row, text="Copy", bg=ACCENT, fg="#ffffff",
                             font=FONT_SMALL, padx=16, pady=10, cursor="hand2")
        copy_btn.pack(side="right", padx=6, pady=6)
        copy_btn.bind("<Button-1>", lambda e: self._copy_generated())

        self.gen_strength_label = tk.Label(inner, text="", font=FONT_BODY,
                                            bg=BG_CARD, fg=TEXT_MUTED)
        self.gen_strength_label.pack(anchor="w", pady=(10, 20))

        # options
        options_row = tk.Frame(inner, bg=BG_CARD)
        options_row.pack(fill="x", pady=(0, 20))

        len_col = tk.Frame(options_row, bg=BG_CARD)
        len_col.pack(side="left", fill="x", expand=True)
        tk.Label(len_col, text="LENGTH", font=("Segoe UI", 9, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        self.length_var = tk.IntVar(value=14)
        self.length_display = tk.Label(len_col, text="14 characters", font=FONT_BODY,
                                        bg=BG_CARD, fg=TEXT_MAIN)
        self.length_display.pack(anchor="w", pady=(4, 4))
        length_scale = tk.Scale(
            len_col, from_=6, to=32, orient="horizontal", variable=self.length_var,
            bg=BG_CARD, fg=TEXT_MAIN, troughcolor="#242b45", highlightthickness=0,
            bd=0, showvalue=False, command=lambda v: self.length_display.config(
                text=f"{int(float(v))} characters")
        )
        length_scale.pack(fill="x")

        toggles_col = tk.Frame(options_row, bg=BG_CARD)
        toggles_col.pack(side="left", fill="x", expand=True, padx=(40, 0))
        tk.Label(toggles_col, text="INCLUDE", font=("Segoe UI", 9, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 6))

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        for text, var in [
            ("Uppercase (A-Z)", self.use_upper),
            ("Lowercase (a-z)", self.use_lower),
            ("Numbers (0-9)", self.use_digits),
            ("Symbols (!@#$)", self.use_symbols),
        ]:
            tk.Checkbutton(
                toggles_col, text=text, variable=var, bg=BG_CARD, fg=TEXT_MAIN,
                selectcolor=BG_CARD, activebackground=BG_CARD, font=FONT_BODY,
                anchor="w"
            ).pack(fill="x", pady=2)

        gen_btn = tk.Label(inner, text="⚡  Generate Password", bg=ACCENT,
                            fg="#ffffff", font=("Segoe UI", 12, "bold"),
                            padx=20, pady=12, cursor="hand2")
        gen_btn.pack(anchor="w")
        gen_btn.bind("<Button-1>", lambda e: self._do_generate())

    def _do_generate(self):
        pwd = generate_password(
            length=self.length_var.get(),
            use_upper=self.use_upper.get(),
            use_lower=self.use_lower.get(),
            use_digits=self.use_digits.get(),
            use_symbols=self.use_symbols.get(),
        )
        self.gen_pwd_var.set(pwd)
        report = check_password_strength(pwd)
        color = STRENGTH_COLORS[report["strength"]]
        self.gen_strength_label.config(text=f"Strength: {report['strength']}", fg=color)
        self._add_history("Generated", pwd, report["strength"])

    def _copy_generated(self):
        pwd = self.gen_pwd_var.get()
        if pwd and "Click Generate" not in pwd:
            self.clipboard_clear()
            self.clipboard_append(pwd)

    # ---------------- TIPS FRAME ----------------
    def _build_tips_frame(self):
        frame = tk.Frame(self.content, bg=BG_MAIN)
        self.frames["tips"] = frame

        tk.Label(frame, text="Security Tips", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_MAIN).pack(anchor="w")
        tk.Label(frame, text="Best practices for staying secure online.",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        tips = [
            ("🔢", "Use at least 12–16 characters",
             "Longer passwords are exponentially harder to brute-force."),
            ("🔀", "Mix character types",
             "Combine uppercase, lowercase, numbers, and symbols."),
            ("🚫", "Never reuse passwords",
             "A breach on one site shouldn't compromise your other accounts."),
            ("🧠", "Avoid dictionary words & personal info",
             "Names, birthdays, and common words are the first things attackers try."),
            ("🔑", "Use a password manager",
             "Let a manager generate and store unique passwords for every account."),
            ("📱", "Enable two-factor authentication (2FA)",
             "Even a leaked password isn't enough if 2FA is turned on."),
        ]

        grid = tk.Frame(frame, bg=BG_MAIN)
        grid.pack(fill="both", expand=True)

        for i, (icon, title, desc) in enumerate(tips):
            r, c = divmod(i, 2)
            card = self._card(grid)
            card.grid(row=r, column=c, padx=(0, 20 if c == 0 else 0),
                      pady=(0, 16), sticky="nsew")
            grid.grid_columnconfigure(c, weight=1)
            inner = tk.Frame(card, bg=BG_CARD, padx=20, pady=16)
            inner.pack(fill="both", expand=True)
            tk.Label(inner, text=icon, font=("Segoe UI", 20), bg=BG_CARD,
                     fg=ACCENT).pack(anchor="w")
            tk.Label(inner, text=title, font=("Segoe UI", 12, "bold"),
                     bg=BG_CARD, fg=TEXT_MAIN, anchor="w").pack(anchor="w", pady=(8, 4))
            tk.Label(inner, text=desc, font=FONT_SMALL, bg=BG_CARD,
                     fg=TEXT_MUTED, anchor="w", justify="left",
                     wraplength=300).pack(anchor="w")

    # ---------------- HISTORY FRAME ----------------
    def _build_history_frame(self):
        frame = tk.Frame(self.content, bg=BG_MAIN)
        self.frames["history"] = frame

        header = tk.Frame(frame, bg=BG_MAIN)
        header.pack(fill="x")
        tk.Label(header, text="History", font=FONT_TITLE,
                 bg=BG_MAIN, fg=TEXT_MAIN).pack(side="left")
        clear_btn = tk.Label(header, text="Clear All", bg=BG_CARD, fg=TEXT_MUTED,
                              font=FONT_SMALL, padx=14, pady=8, cursor="hand2")
        clear_btn.pack(side="right", pady=6)
        clear_btn.bind("<Button-1>", lambda e: self._clear_history())

        tk.Label(frame, text="Session log of checked and generated passwords "
                              "(cleared when you close the app).",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        warn = tk.Label(frame, text="⚠ Passwords are shown in full below. Close this "
                                     "app when done if others can see your screen.",
                        font=FONT_SMALL, bg=BG_MAIN, fg=MED_COLOR)
        warn.pack(anchor="w", pady=(0, 10))

        columns = ("time", "source", "value", "strength")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG_CARD, fieldbackground=BG_CARD,
                        foreground=TEXT_MAIN, rowheight=32, borderwidth=0, font=FONT_BODY)
        style.configure("Treeview.Heading", background=BG_SIDEBAR, foreground=ACCENT,
                        font=("Consolas", 9, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT_SOFT)])

        self.history_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col, label, width in [
            ("time", "Time", 90), ("source", "Type", 100),
            ("value", "Password", 260), ("strength", "Strength", 100)
        ]:
            self.history_tree.heading(col, text=label)
            self.history_tree.column(col, width=width, anchor="w")
        self.history_tree.pack(fill="both", expand=True)

        self.history_tree.tag_configure("Weak", foreground=WEAK_COLOR)
        self.history_tree.tag_configure("Medium", foreground=MED_COLOR)
        self.history_tree.tag_configure("Strong", foreground=STRONG_COLOR)

    def _add_history(self, source, pwd, strength):
        entry = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "source": source,
            "value": pwd,
            "strength": strength,
        }
        self.history.append(entry)
        if self.current_frame_key == "history":
            self._refresh_history_view()

    def _refresh_history_view(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        for entry in reversed(self.history):
            self.history_tree.insert(
                "", "end",
                values=(entry["time"], entry["source"], entry["value"], entry["strength"]),
                tags=(entry["strength"],)
            )

    def _clear_history(self):
        self.history.clear()
        self._refresh_history_view()


if __name__ == "__main__":
    app = PasswordDashboard()
    app.mainloop()
