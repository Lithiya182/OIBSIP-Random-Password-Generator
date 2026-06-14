# Tessera — Password Generator

A modern GUI-based password generator built with Python and Tkinter, styled
with the Tessera dark teal color scheme.

## Features

- Generate cryptographically secure random passwords (`secrets`, not `random`)
- Guarantees at least one character from every selected category (uppercase,
  lowercase, numbers, symbols), so a "Strong" password always actually
  contains what it promises
- Adjustable password length via slider or direct entry, with live validation
- Include/exclude:
  - Uppercase letters (A–Z)
  - Lowercase letters (a–z)
  - Numbers (0–9)
  - Symbols (!@#$…)
- "Select All / Deselect All" toggle for the character options
- Exclude similar characters (O, 0, l, I, 1)
- Password strength indicator (text label + colored progress bar)
- Show/hide toggle for the generated password
- Copy password to clipboard, with on-screen confirmation
- Recent password history (last 5), masked by default — click to reveal/hide,
  with its own copy-confirmation feedback
- Errors and validation messages shown in a dedicated status area, separate
  from the password field
- Tessera dark teal design system

## Color Scheme

| Token   | Hex       | Role                          |
|---------|-----------|-------------------------------|
| BG      | `#061e29` | Page / window background      |
| SURFACE | `#0d2e3e` | Cards, frames                 |
| MID     | `#1d546d` | Primary buttons               |
| ACCENT  | `#5f9598` | Highlights, bars, labels      |
| LIGHT   | `#f3f4f4` | Primary text                  |
| MUTED   | `#a8bfc0` | Secondary / placeholder text  |

## Technologies Used

- Python 3.9+
- Tkinter / ttk (standard library)
- Pyperclip

## Installation

Clone the repository:

```bash
git clone git clone https://github.com/Lithiya182/OIBSIP-Random-Password-Generator.git
cd tessera-password-generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

> **Tip:** Press `Enter` at any time to generate a new password.

## Security Notes

- Passwords are generated using Python's `secrets` module, which is suitable
  for cryptographic use (unlike `random`).
- The generated password and recent-password history are masked by default
  to reduce shoulder-surfing risk; click to reveal individual entries.
- Password history is kept in memory only for the current session and is
  never written to disk.

## License

This project is available under the MIT License. Feel free to use, modify,
and distribute it for personal or educational purposes.

## Author

Created as part of the Oasis Infobyte Internship Program.