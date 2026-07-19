# 🔐 Password Strength Checker & Generator Dashboard

**DecodeLabs Cyber Security Internship** · Project 1

![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-success)
![GUI](https://img.shields.io/badge/Interface-Tkinter-purple)

A sleek desktop dashboard that analyzes password strength in real time and generates secure random passwords — built entirely in Python.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Strength Checker** | Live analysis with a color-coded strength bar and detailed criteria checklist |
| 🔑 **Password Generator** | Creates strong random passwords with adjustable length and character rules |
| 🚫 **Leaked Password Detection** | Flags passwords found in common breach lists |
| 💡 **Security Tips** | Curated best practices for staying secure online |
| 📊 **Session History** | Tracks passwords checked/generated during your session |

---

## 🖥️ Preview

> Dark, modern dashboard interface with sidebar navigation and live feedback.

---

## 🚀 How to Run

**Requirements:** Python 3.6+

```bash
python password_dashboard.py
```

Make sure `app_icon.ico` and `app_icon.png` are in the same folder as the script.

---

## 🧠 How It Works

- **Length is a hard gate** — passwords under 8 characters are automatically classified as *Weak*
- **Scoring system (0–5 points)** — based on length, uppercase/lowercase mix, numbers, and symbols
- **Thresholds:** `0–2 = Weak` · `3–4 = Medium` · `5 = Strong`
- Common/leaked passwords are always flagged as *Weak*, regardless of score

---

## 🛠️ Built With

- **Python** — core logic
- **Tkinter** — GUI framework
- String handling, conditional logic & input validation

---

## 👩‍💻 Author

**Sonia Farheen**  
DecodeLabs — Batch 2026

---

⭐ *Part of an ongoing Cyber Security internship project series.*
