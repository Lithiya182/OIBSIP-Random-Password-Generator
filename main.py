import tkinter as tk
import random
import string
import pyperclip

generated_password = ""
def generate_password():
    global generated_password

    characters = ""

    if uppercase_var.get():
        characters += string.ascii_uppercase

    if lowercase_var.get():
        characters += string.ascii_lowercase

    if numbers_var.get():
        characters += string.digits

    if symbols_var.get():
        characters += string.punctuation

    if characters == "":
        result_var.set("Select at least one option!")
        strength_label.config(text="Strength:")
        return
    if exclude_similar_var.get():
        similar_chars = "O0Il1"

        for char in similar_chars:
            characters = characters.replace(char, "")

    try:
        length = int(length_entry.get())
        if length <= 0:
            result_var.set("Length must be greater than 0!")
            strength_label.config(text="Strength:")
            return

    except ValueError:
        result_var.set("Enter a valid length!")
        strength_label.config(text="Strength:")
        return

    password = ''.join(
        random.choice(characters)
        for _ in range(length)
    )

    generated_password = password

    result_entry.config(state="normal")
    result_var.set(password)
    result_entry.config(state="readonly")

    strength_label.config(
        text=f"Strength: {check_strength(password)}"
    )
    strength = check_strength(password)

    if "Weak" in strength:
        strength_label.config(
            text=f"Strength: {strength}",
            fg="#ff6b6b"
        )

    elif "Medium" in strength:
        strength_label.config(
            text=f"Strength: {strength}",
            fg="#f7b267"
        )

    else:
        strength_label.config(
            text=f"Strength: {strength}",
            fg="#7ECECA"
        )

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        return "Weak 🔴"
    elif score <= 4:
        return "Medium 🟡"
    else:
        return "Strong 🟢"

def copy_password():
    if generated_password:
        pyperclip.copy(generated_password)

        strength_label.config(
            text="Copied to Clipboard ✓",
            fg="#7ECECA"
        )

root = tk.Tk()

root.title("Random Password Generator")
root.geometry("650x550")
root.configure(bg="#2A2B3B")
root.resizable(False, False)

title = tk.Label(
    root,
    text="PASSWORD GENERATOR",
    font=("Segoe UI", 24, "bold"),
    bg="#2A2B3B",
    fg="#7ECECA"
)
title.pack(pady=20)

length_label = tk.Label(
    root,
    text="Password Length",
    font=("Segoe UI", 11),
    bg="#2A2B3B",
    fg="white"
)
length_label.pack()



length_entry = tk.Entry(
    root,
    font=("Segoe UI", 12),
    bg="#49566C",
    fg="white",
    insertbackground="white",
    relief="flat"
)
length_entry.pack(pady=5)
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_similar_var = tk.BooleanVar()

options_frame = tk.Frame(
    root,
    bg="#2A2B3B"
)

options_frame.pack(pady=10)

tk.Checkbutton(

    options_frame,
    text="Include Uppercase Letters",
    variable=uppercase_var,
    bg="#2A2B3B",
    fg="white",
    activebackground="#2A2B3B",
    activeforeground="white",
    selectcolor="#49566C",
    font=("Segoe UI", 10)
).pack(anchor="w")

tk.Checkbutton(

    options_frame,
    text="Include Lowercase Letters",
    variable=lowercase_var,
    bg="#2A2B3B",
    fg="white",
    activebackground="#2A2B3B",
    activeforeground="white",
    selectcolor="#49566C",
    font=("Segoe UI", 10)
).pack(anchor="w")

tk.Checkbutton(

    options_frame,
    text="Include Numbers",
    variable=numbers_var,
    bg="#2A2B3B",
    fg="white",
    activebackground="#2A2B3B",
    activeforeground="white",
    selectcolor="#49566C",
    font=("Segoe UI", 10)
).pack(anchor="w")

tk.Checkbutton(

    options_frame,
    text="Include Symbols",
    variable=symbols_var,
    bg="#2A2B3B",
    fg="white",
    activebackground="#2A2B3B",
    activeforeground="white",
    selectcolor="#49566C",
    font=("Segoe UI", 10)
).pack(anchor="w")

tk.Checkbutton(

    options_frame,
    text="Exclude Similar Characters (O, 0, l, I, 1)",
    variable=exclude_similar_var,
    bg="#2A2B3B",
    fg="white",
    activebackground="#2A2B3B",
    activeforeground="white",
    selectcolor="#49566C",
    font=("Segoe UI", 10)
).pack(anchor="w")

generate_btn = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    font=("Segoe UI", 11, "bold"),
    bg="#577085",
    fg="white",
    activebackground="#72AEB6",
    relief="flat",
    padx=15,
    pady=8
)
generate_btn.pack(pady=15)

copy_btn = tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    font=("Segoe UI", 11, "bold"),
    bg="#577085",
    fg="white",
    activebackground="#72AEB6",
    relief="flat",
    padx=15,
    pady=8
)

copy_btn.pack(pady=5)

password_frame = tk.Frame(
    root,
    bg="#3A3F54",
    padx=10,
    pady=10
)

password_frame.pack(pady=15)

result_var = tk.StringVar()

result_entry = tk.Entry(
    password_frame,
    textvariable=result_var,
    font=("Consolas", 13, "bold"),
    justify="center",
    bg="#3A3F54",
    fg="black",
    relief="flat",
    width=40
)

result_entry.pack()


strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Segoe UI", 11, "bold"),
    bg="#2A2B3B",
    fg="#7ECECA"
)

strength_label.pack(pady=5)

root.mainloop()