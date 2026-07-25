# 🔐 Encryption & Decryption Dashboard

**DecodeLabs Cyber Security Internship** · Project 2

![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-success)
![GUI](https://img.shields.io/badge/Interface-Tkinter-purple)

A desktop dashboard that encrypts and decrypts text using a Caesar cipher, with a bonus Vigenère cipher mode — built entirely in Python.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔑 **Caesar Cipher** | Encrypt/decrypt text with a user-adjustable shift key (1–25) |
| 🧩 **Vigenère Cipher (Bonus)** | Stronger keyword-based cipher, a different shift per letter |
| 📘 **How It Works** | Step-by-step breakdown of the IPO model behind the cipher |
| 🔤 **Edge case handling** | Spaces, numbers, and punctuation are left untouched; letter case is preserved |

---

## 🚀 How to Run

**Requirements:** Python 3.6+

```bash
python caesar_cipher_dashboard.py
```

Keep these files in the same folder as the script:
- `encryption_icon.ico` / `encryption_icon.png`
- `encryption_icon_outline_small.png` / `decryption_icon_small.png`

---

## 🧠 How It Works

- **Encryption:** `E(x) = (x + n) % 26`
- **Decryption:** `D(x) = (x - n) % 26` — the same key locks and unlocks (symmetric encryption)
- Each character is converted to its ASCII position with `ord()`, shifted, then converted back with `chr()`
- The `% 26` wraps the alphabet around (`Z + 1 → A`)

---

## 🛠️ Built With

- **Python** — core cipher logic
- **Tkinter** — GUI framework
- ASCII math (`ord()` / `chr()`), modular arithmetic, string handling

---

## ⚠️ Security Note

A Caesar cipher has only 25 possible keys, making it easy to break with brute force or frequency analysis. It demonstrates the *logic* of encryption; real-world systems use much stronger methods (e.g. AES).

---

## 👩‍💻 Author

**Sonia Farheen**
DecodeLabs — Batch 2026

---

⭐ *Part of an ongoing Cyber Security internship project series.*
