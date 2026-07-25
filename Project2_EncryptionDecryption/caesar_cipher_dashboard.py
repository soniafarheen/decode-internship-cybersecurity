"""
Encryption & Decryption Dashboard - Project 2 (Cyber Security Track)

Goal (per project brief):
  Implement a simple encryption and decryption technique.
  Key Requirements:
    - Encrypt user text using a basic logic (Caesar cipher)
    - Decrypt the encrypted text
    - Display both encrypted and decrypted output
  Key Skills: encryption concepts, logic building, data protection basics

Implementation notes (follows the IPO model + math taught in the brief):
  INPUT   -> plaintext (raw characters)
  PROCESS -> ord() converts each character to its ASCII position,
             shift is applied with modular arithmetic (% 26) so the
             alphabet "wraps around" (Z + 1 -> A), then chr() converts
             the number back to a character.
  OUTPUT  -> ciphertext (or, in reverse, plaintext again)

  Encryption: E(x) = (x + shift) % 26
  Decryption: D(x) = (x - shift) % 26   -- same key locks and unlocks
              (symmetric encryption, exactly as described in the brief)

  Edge cases handled: spaces, numbers, and punctuation are left
  untouched (only letters A-Z / a-z are shifted), and letter case
  is preserved.

A bonus Vigenere cipher (keyword-based, multiple shifts) is included
as the "unique/experiment" extension suggested in the brief's
conclusion, alongside a short "How It Works" explainer tab.
"""

import tkinter as tk
from tkinter import ttk
import os

# ---------------------------------------------------------------------------
# THEME -- Light blue/white gradient (inspired by modern mobile app UI)
# ---------------------------------------------------------------------------
BG_SIDEBAR = "#ffffff"
BG_MAIN = "#eef4fb"
BG_CARD = "#ffffff"
ACCENT = "#2f80ed"
ACCENT_SOFT = "#e4f0ff"
GRADIENT_TOP = "#1e3c72"
GRADIENT_BOTTOM = "#2f80ed"
CARD_BORDER = "#dbe4ee"
TEXT_MAIN = "#1b2733"
TEXT_MUTED = "#7c8896"
GOOD_COLOR = "#1e9e64"
WARN_COLOR = "#d98a1f"

FONT_TITLE = ("Times New Roman", 24, "bold")
FONT_SUB = ("Times New Roman", 12, "bold")
FONT_H2 = ("Times New Roman", 16, "bold")
FONT_BODY = ("Times New Roman", 13, "bold")
FONT_SMALL = ("Times New Roman", 11, "bold")
FONT_MONO = ("Times New Roman", 14, "bold")


# ---------------------------------------------------------------------------
# CORE CIPHER LOGIC
# ---------------------------------------------------------------------------
def caesar_shift_char(char: str, shift: int) -> str:
    """Shift a single character by `shift` positions, wrapping with % 26.
    Non-letters (spaces, digits, punctuation) are returned unchanged."""
    if char.isupper():
        base = ord('A')
        return chr((ord(char) - base + shift) % 26 + base)
    elif char.islower():
        base = ord('a')
        return chr((ord(char) - base + shift) % 26 + base)
    else:
        return char  # edge case: leave spaces/numbers/punctuation as-is


def caesar_encrypt(text: str, shift: int) -> str:
    return "".join(caesar_shift_char(c, shift) for c in text)


def caesar_decrypt(text: str, shift: int) -> str:
    # Decryption is just encryption with the negative shift.
    # Python's % operator already returns a positive result for
    # negative numbers, so (x - shift) % 26 works correctly here.
    return "".join(caesar_shift_char(c, -shift) for c in text)


def vigenere_process(text: str, key: str, encrypt: bool = True) -> str:
    """Bonus cipher: each letter is shifted by a different amount,
    taken from the repeating keyword (e.g. key 'ABC' -> shifts 0,1,2,0,1,2...).
    This is the 'unique solution' the project brief's conclusion invites."""
    if not key:
        return text
    key = "".join(c for c in key.upper() if c.isalpha()) or "A"
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            k_shift = ord(key[key_index % len(key)]) - ord('A')
            shift = k_shift if encrypt else -k_shift
            result.append(caesar_shift_char(char, shift))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


# ---------------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------------
class CipherDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Encryption & Decryption Dashboard")
        self.geometry("980x640")
        self.minsize(900, 600)
        self.configure(bg=BG_MAIN)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "encryption_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.encrypt_btn_icon = self._load_button_icon("encryption_icon_outline_small.png")
        self.decrypt_btn_icon = self._load_button_icon("decryption_icon_small.png")

        self.frames = {}
        self._build_sidebar()
        self._build_content_area()
        self._build_caesar_frame()
        self._build_vigenere_frame()
        self._build_learn_frame()
        self.show_frame("caesar")

    # ---------------- GRADIENT HELPER ----------------
    def _load_button_icon(self, filename):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        if os.path.exists(path):
            try:
                return tk.PhotoImage(file=path)
            except Exception:
                return None
        return None

    def _draw_gradient(self, canvas, width, height, color1, color2):
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

        header_h = 190
        header_canvas = tk.Canvas(sidebar, width=220, height=header_h,
                                   highlightthickness=0, bd=0)
        header_canvas.pack(fill="x")
        self._draw_gradient(header_canvas, 220, header_h, GRADIENT_TOP, GRADIENT_BOTTOM)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "encryption_icon.png")
        self.logo_img = None
        if os.path.exists(icon_path):
            try:
                raw = tk.PhotoImage(file=icon_path)
                self.logo_img = raw.subsample(2, 2)  # 256px -> 128px (larger, prominent logo)
            except Exception:
                self.logo_img = None

        if self.logo_img:
            header_canvas.create_image(110, 68, image=self.logo_img)
        else:
            header_canvas.create_text(110, 60, text="🔐", font=("Segoe UI", 34), fill="#ffffff")

        header_canvas.create_text(110, 145, text="CipherLab",
                                   font=("Segoe UI", 15, "bold"), fill="#ffffff")
        header_canvas.create_text(110, 167, text="Encryption Dashboard",
                                   font=FONT_SMALL, fill="#d8d3ff")

        tk.Frame(sidebar, bg=BG_SIDEBAR, height=14).pack(fill="x")

        self.nav_buttons = {}
        nav_items = [
            ("caesar", "🔑  Caesar Cipher"),
            ("vigenere", "🧩  Vigenère (Bonus)"),
            ("learn", "📘  How It Works"),
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
        for f in self.frames.values():
            f.pack_forget()
        for k, b in self.nav_buttons.items():
            b.config(bg=ACCENT_SOFT if k == key else BG_SIDEBAR,
                     fg=TEXT_MAIN if k == key else TEXT_MUTED)
        self.frames[key].pack(fill="both", expand=True, padx=30, pady=26)

    def _build_content_area(self):
        self.content = tk.Frame(self, bg=BG_MAIN)
        self.content.pack(side="left", fill="both", expand=True)

    def _card(self, parent):
        return tk.Frame(parent, bg=BG_CARD, highlightbackground=ACCENT,
                         highlightthickness=2, bd=0)

    # ---------------- CAESAR CIPHER FRAME ----------------
    def _build_caesar_frame(self):
        frame = tk.Frame(self.content, bg=BG_MAIN)
        self.frames["caesar"] = frame

        tk.Label(frame, text="🔑 Caesar Cipher", font=FONT_TITLE,
                 bg=BG_MAIN, fg=GRADIENT_TOP).pack(anchor="w")
        tk.Label(frame, text="Encrypt and decrypt text using a shift-based cipher.",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        card = self._card(frame)
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=BG_CARD, padx=24, pady=24)
        inner.pack(fill="both", expand=True)

        # --- Input ---
        tk.Label(inner, text="📝  PLAINTEXT (input)", font=("Times New Roman", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        self.plain_text = tk.Text(inner, height=4, font=FONT_MONO, bg="#f2f6fb",
                                   fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                   relief="flat", wrap="word")
        self.plain_text.pack(fill="x", pady=(6, 16))

        # --- Shift key control ---
        shift_row = tk.Frame(inner, bg=BG_CARD)
        shift_row.pack(fill="x", pady=(0, 16))
        tk.Label(shift_row, text="🔢  SHIFT KEY (n)", font=("Times New Roman", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(side="left")
        self.shift_var = tk.IntVar(value=3)
        self.shift_display = tk.Label(shift_row, text="3", font=("Consolas", 12, "bold"),
                                       bg=BG_CARD, fg=ACCENT, width=3)
        self.shift_display.pack(side="right")
        shift_scale = tk.Scale(
            shift_row, from_=1, to=25, orient="horizontal", variable=self.shift_var,
            bg=BG_CARD, fg=TEXT_MAIN, troughcolor="#f2f6fb", highlightthickness=0,
            bd=0, showvalue=False,
            command=lambda v: self.shift_display.config(text=str(int(float(v))))
        )
        shift_scale.pack(side="left", fill="x", expand=True, padx=12)

        # --- Buttons ---
        btn_row = tk.Frame(inner, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(0, 16))
        encrypt_btn = tk.Label(btn_row, text="  Encrypt", image=self.encrypt_btn_icon,
                                compound="left", bg=ACCENT, fg="#ffffff",
                                font=("Segoe UI", 11, "bold"), padx=18, pady=10, cursor="hand2")
        encrypt_btn.pack(side="left")
        encrypt_btn.bind("<Button-1>", lambda e: self._do_encrypt())

        decrypt_btn = tk.Label(btn_row, text="  Decrypt", image=self.decrypt_btn_icon,
                                compound="left", bg="#f2f6fb", fg=TEXT_MAIN,
                                font=("Segoe UI", 11, "bold"), padx=18, pady=10, cursor="hand2")
        decrypt_btn.pack(side="left", padx=(10, 0))
        decrypt_btn.bind("<Button-1>", lambda e: self._do_decrypt())

        # --- Output: ciphertext ---
        tk.Label(inner, text="🔒  CIPHERTEXT (encrypted output)", font=("Times New Roman", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        self.cipher_text = tk.Text(inner, height=4, font=FONT_MONO, bg="#f2f6fb",
                                    fg=GOOD_COLOR, insertbackground=TEXT_MAIN,
                                    relief="flat", wrap="word")
        self.cipher_text.pack(fill="x", pady=(6, 16))

        # --- Output: decrypted text ---
        tk.Label(inner, text="🔓  DECRYPTED OUTPUT (should match plaintext)",
                 font=("Times New Roman", 11, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        self.decrypted_text = tk.Text(inner, height=4, font=FONT_MONO, bg="#f2f6fb",
                                       fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                       relief="flat", wrap="word")
        self.decrypted_text.pack(fill="x", pady=(6, 0))

    def _do_encrypt(self):
        plain = self.plain_text.get("1.0", "end-1c")
        shift = self.shift_var.get()
        cipher = caesar_encrypt(plain, shift)
        self.cipher_text.delete("1.0", "end")
        self.cipher_text.insert("1.0", cipher)
        self.decrypted_text.delete("1.0", "end")

    def _do_decrypt(self):
        cipher = self.cipher_text.get("1.0", "end-1c")
        shift = self.shift_var.get()
        plain_back = caesar_decrypt(cipher, shift)
        self.decrypted_text.delete("1.0", "end")
        self.decrypted_text.insert("1.0", plain_back)

    # ---------------- VIGENERE (BONUS) FRAME ----------------
    def _build_vigenere_frame(self):
        frame = tk.Frame(self.content, bg=BG_MAIN)
        self.frames["vigenere"] = frame

        tk.Label(frame, text="🧩 Vigenère Cipher  ·  Bonus", font=FONT_TITLE,
                 bg=BG_MAIN, fg=GRADIENT_TOP).pack(anchor="w")
        tk.Label(frame, text="A stronger cipher using a keyword instead of a single shift.",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        card = self._card(frame)
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=BG_CARD, padx=24, pady=24)
        inner.pack(fill="both", expand=True)

        tk.Label(inner, text="📝  PLAINTEXT (input)", font=("Times New Roman", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        self.v_input = tk.Text(inner, height=3, font=FONT_MONO, bg="#f2f6fb",
                                fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                relief="flat", wrap="word")
        self.v_input.pack(fill="x", pady=(6, 16))

        key_row = tk.Frame(inner, bg=BG_CARD)
        key_row.pack(fill="x", pady=(0, 16))
        tk.Label(key_row, text="🗝️  KEYWORD", font=("Times New Roman", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(side="left")
        self.v_key_var = tk.StringVar(value="LOCK")
        v_key_entry = tk.Entry(key_row, textvariable=self.v_key_var, font=FONT_MONO,
                                bg="#f2f6fb", fg=ACCENT, insertbackground=TEXT_MAIN,
                                relief="flat")
        v_key_entry.pack(side="left", fill="x", expand=True, padx=12, ipady=6)

        btn_row = tk.Frame(inner, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(0, 16))
        enc_btn = tk.Label(btn_row, text="  Encrypt", image=self.encrypt_btn_icon,
                            compound="left", bg=ACCENT, fg="#ffffff",
                            font=("Segoe UI", 11, "bold"), padx=18, pady=10, cursor="hand2")
        enc_btn.pack(side="left")
        enc_btn.bind("<Button-1>", lambda e: self._do_vigenere_encrypt())

        dec_btn = tk.Label(btn_row, text="  Decrypt", image=self.decrypt_btn_icon,
                            compound="left", bg="#f2f6fb", fg=TEXT_MAIN,
                            font=("Segoe UI", 11, "bold"), padx=18, pady=10, cursor="hand2")
        dec_btn.pack(side="left", padx=(10, 0))
        dec_btn.bind("<Button-1>", lambda e: self._do_vigenere_decrypt())

        tk.Label(inner, text="🔒  CIPHERTEXT (encrypted output)", font=("Times New Roman", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        self.v_output = tk.Text(inner, height=3, font=FONT_MONO, bg="#f2f6fb",
                                 fg=GOOD_COLOR, insertbackground=TEXT_MAIN,
                                 relief="flat", wrap="word")
        self.v_output.pack(fill="x", pady=(6, 16))

        tk.Label(inner, text="🔓  DECRYPTED OUTPUT (should match plaintext)",
                 font=("Times New Roman", 11, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        self.v_decrypted = tk.Text(inner, height=3, font=FONT_MONO, bg="#f2f6fb",
                                    fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                    relief="flat", wrap="word")
        self.v_decrypted.pack(fill="x", pady=(6, 0))

    def _do_vigenere_encrypt(self):
        text = self.v_input.get("1.0", "end-1c")
        key = self.v_key_var.get()
        result = vigenere_process(text, key, encrypt=True)
        self.v_output.delete("1.0", "end")
        self.v_output.insert("1.0", result)
        self.v_decrypted.delete("1.0", "end")

    def _do_vigenere_decrypt(self):
        # Decrypts whatever is currently in the CIPHERTEXT box (not the
        # plaintext box) -- this was the earlier source of confusion,
        # since encrypting and decrypting the same input box overwrote
        # each other's text.
        cipher = self.v_output.get("1.0", "end-1c")
        key = self.v_key_var.get()
        result = vigenere_process(cipher, key, encrypt=False)
        self.v_decrypted.delete("1.0", "end")
        self.v_decrypted.insert("1.0", result)

    # ---------------- LEARN FRAME ----------------
    def _build_learn_frame(self):
        frame = tk.Frame(self.content, bg=BG_MAIN)
        self.frames["learn"] = frame

        tk.Label(frame, text="📘 How It Works", font=FONT_TITLE,
                 bg=BG_MAIN, fg=GRADIENT_TOP).pack(anchor="w")
        tk.Label(frame, text="The IPO model behind every cryptographic system.",
                 font=FONT_SUB, bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 20))

        steps = [
            ("1. INPUT", "Plaintext (raw characters)",
             "Your original text, e.g. 'HELLO'."),
            ("2. ASCII CONVERSION", "ord('A') = 65",
             "Every character becomes a number before any math can happen."),
            ("3. SHIFT + WRAP", "E(x) = (x + n) % 26",
             "The shift key (n) is added, and % 26 wraps Z back to A "
             "so the alphabet never runs out."),
            ("4. BACK TO TEXT", "chr(68) = 'D'",
             "The resulting number is converted back into a letter."),
            ("5. OUTPUT", "Ciphertext (secured)",
             "Decryption simply reverses the shift: D(x) = (x - n) % 26 "
             "— the same key that locks it also unlocks it."),
        ]

        card = self._card(frame)
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=BG_CARD, padx=24, pady=24)
        inner.pack(fill="both", expand=True)

        for title, formula, desc in steps:
            row = tk.Frame(inner, bg=BG_CARD)
            row.pack(fill="x", pady=10, anchor="w")
            tk.Label(row, text=title, font=("Segoe UI", 10, "bold"),
                     bg=BG_CARD, fg=ACCENT, width=20, anchor="w").pack(side="left")
            col = tk.Frame(row, bg=BG_CARD)
            col.pack(side="left", fill="x", expand=True)
            tk.Label(col, text=formula, font=("Consolas", 12, "bold"),
                     bg=BG_CARD, fg=TEXT_MAIN, anchor="w").pack(anchor="w")
            tk.Label(col, text=desc, font=FONT_SMALL, bg=BG_CARD, fg=TEXT_MUTED,
                     anchor="w", justify="left", wraplength=560).pack(anchor="w")

        tk.Label(inner, text="⚠ Note: a Caesar cipher has only 25 possible keys, "
                             "so it is easily broken by brute force or frequency "
                             "analysis. It teaches the logic; real systems use "
                             "much stronger methods (e.g. AES).",
                 font=FONT_SMALL, bg=BG_CARD, fg=WARN_COLOR, wraplength=700,
                 justify="left").pack(anchor="w", pady=(20, 0))


if __name__ == "__main__":
    app = CipherDashboard()
    app.mainloop()
