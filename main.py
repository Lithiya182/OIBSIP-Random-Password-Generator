import tkinter as tk
from tkinter import ttk
import secrets
import string
import pyperclip

# ── State 
current_password = ""
_syncing = False

# ── Palette 
BG       = "#0b1f2d"   
CARD     = "#112233"   
FIELD    = "#0d1f2f"   
BTN_MID  = "#1a4a6b"   
ACCENT   = "#4a9abb"   
LIGHT    = "#ddeef6"   
MUTED    = "#6a9ab0"   
BORDER   = "#1e3a52"   
ERR      = "#d95f5f"

MASK = "•"

# ── Helpers 
def get_score(pw):
    s = 0
    if len(pw) >= 8:  s += 1
    if len(pw) >= 12: s += 1
    if any(c.isupper() for c in pw):             s += 1
    if any(c.islower() for c in pw):             s += 1
    if any(c.isdigit() for c in pw):             s += 1
    if any(c in string.punctuation for c in pw): s += 1
    return s

def strength_text(pw):
    s = get_score(pw)
    if s <= 2: return "Weak",   "#c0392b"
    if s <= 4: return "Fair",   "#e67e22"
    return            "Strong", ACCENT

def update_strength(pw):
    label, color = strength_text(pw)
    strength_lbl.config(text=f"Strength: {label}", fg=color)
    strength_cv.delete("bar")
    strength_cv.update_idletasks()
    actual_w = strength_cv.winfo_width() or BAR_W
    w = int(actual_w * get_score(pw) / 6)
    if w:
        strength_cv.create_rectangle(0, 0, w, BAR_H, fill=color, outline="", tags="bar")

def clear_strength():
    strength_lbl.config(text="Strength:", fg=ACCENT)
    strength_cv.delete("bar")

def reset_strength():
    update_strength(current_password) if current_password else clear_strength()

def show_err(msg): status_lbl.config(text=msg, fg=ERR)
def clear_err():   status_lbl.config(text="")

# ── Enable / disable 
def set_gen(on):
    generate_btn.config(state="normal" if on else "disabled",
                        bg=BTN_MID if on else CARD,
                        fg=LIGHT   if on else MUTED)

def set_copy(on):
    copy_btn.config(state="normal" if on else "disabled",
                    bg=BTN_MID if on else CARD,
                    fg=LIGHT   if on else MUTED)

def set_eye(on):
    toggle_eye.config(state="normal" if on else "disabled",
                      fg=MUTED if on else BORDER)

# ── Length entry validation 
def validate(val):
    if not val.strip():       return False, None, "Enter a length!"
    try:   n = int(val)
    except: return False, None, "Enter a whole number!"
    if n <= 0:   return False, None, "Length must be > 0!"
    if n > 128:  return False, None, "Max length is 128!"
    return True, n, ""

def on_entry_change(*_):
    global _syncing
    if _syncing: return
    ok, n, err = validate(len_var.get())
    if ok:
        clear_err(); set_gen(True)
        if 4 <= n <= 64:
            _syncing = True; length_scale.set(n); _syncing = False
    else:
        if len_var.get().strip(): show_err(err)
        set_gen(False)

def on_scale(val):
    global _syncing
    if _syncing: return
    _syncing = True; len_var.set(str(int(float(val)))); _syncing = False

# ── Password display 
def refresh_display():
    pw_entry.config(state="normal")
    if current_password:
        pw_entry.config(fg=LIGHT)
        pw_var.set(current_password if eye_var.get() else MASK * len(current_password))
    else:
        pw_var.set("Click Generate to create a password")
        pw_entry.config(fg=MUTED)
    pw_entry.config(state="readonly")

def toggle_eye_fn():
    if not current_password: return
    eye_var.set(not eye_var.get())
    toggle_eye.config(text="🙈" if eye_var.get() else "👁")
    refresh_display()

# ── Categories 
def get_cats():
    cats = []
    if upper_var.get(): cats.append(string.ascii_uppercase)
    if lower_var.get(): cats.append(string.ascii_lowercase)
    if num_var.get():   cats.append(string.digits)
    if sym_var.get():   cats.append(string.punctuation)
    if excl_var.get():
        cats = [c.translate(str.maketrans("","","O0Il1")) for c in cats]
        cats = [c for c in cats if c]
    return cats

# ── Generate 
def generate(_e=None):
    global current_password
    cats = get_cats()
    if not cats:
        show_err("Select at least one character type!"); return
    ok, n, err = validate(len_var.get())
    if not ok:
        show_err(err); return
    if n < len(cats):
        show_err(f"Length must be ≥ {len(cats)} for selected options!"); return

    pool = "".join(cats)
    chars = [secrets.choice(c) for c in cats]
    chars += [secrets.choice(pool) for _ in range(n - len(cats))]
    secrets.SystemRandom().shuffle(chars)
    current_password = "".join(chars)

    clear_err()
    eye_var.set(True); toggle_eye.config(text="🙈")
    refresh_display()
    set_copy(True); set_eye(True)
    update_strength(current_password)
    add_history(current_password)

# ── Copy 
def copy_pw():
    if not current_password: return
    pyperclip.copy(current_password)
    strength_lbl.config(text="Copied to clipboard ✓", fg=ACCENT)
    root.after(1800, reset_strength)

# ── History 
history: list[dict] = []

def add_history(pw):
    history.insert(0, {"pw": pw, "show": False})
    if len(history) > 5: history.pop()
    draw_history()

def toggle_hist(i):
    history[i]["show"] = not history[i]["show"]
    draw_history()

def copy_hist(pw, btn):
    pyperclip.copy(pw)
    btn.config(text="Copied!")
    root.after(1200, lambda: btn.config(text="Copy"))

def draw_history():
    for w in hist_inner.winfo_children(): w.destroy()
    if not history:
        tk.Label(hist_inner, text="No passwords yet",
                 font=("Segoe UI", 9), bg=CARD, fg=MUTED).pack(pady=14)
        return
    for i, e in enumerate(history):
        disp = e["pw"] if e["show"] else MASK * len(e["pw"])
        row  = tk.Frame(hist_inner, bg=CARD)
        row.pack(fill=tk.X, pady=1)
        lbl = tk.Label(row, text=disp, font=("Consolas", 9),
                       bg=CARD, fg=ACCENT, anchor="w", cursor="hand2")
        lbl.pack(side=tk.LEFT, padx=6, fill=tk.X, expand=True)
        lbl.bind("<Button-1>", lambda _e, idx=i: toggle_hist(idx))
        eye_b = tk.Button(row, text="🙈" if e["show"] else "👁",
                          font=("Segoe UI", 8), bg=CARD, fg=MUTED,
                          relief="flat", bd=0, activebackground=CARD,
                          command=lambda idx=i: toggle_hist(idx))
        eye_b.pack(side=tk.RIGHT, padx=2)
        cb = tk.Button(row, text="Copy", font=("Segoe UI", 8),
                       bg=BTN_MID, fg=LIGHT, relief="flat", padx=6,
                       activebackground=ACCENT)
        cb.config(command=lambda p=e["pw"], b=cb: copy_hist(p, b))
        cb.pack(side=tk.RIGHT, padx=4, pady=2)

# ── Select all toggle 
char_vars_list = []   # filled after BooleanVars are created

def toggle_all():
    on = not all(v.get() for v in char_vars_list)
    for v in char_vars_list: v.set(on)
    sel_btn.config(text="Deselect All" if on else "Select All")

def sync_sel_btn(*_):
    sel_btn.config(text="Deselect All" if all(v.get() for v in char_vars_list) else "Select All")


# UI

root = tk.Tk()
root.title("Tessera — Password Generator")
root.configure(bg=BG)
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("T.Horizontal.TScale",
                background=CARD, troughcolor=BORDER,
                sliderthickness=14, sliderrelief="flat")

# ── Outer padding frame 
outer = tk.Frame(root, bg=BG)
outer.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# ── Header 
hdr = tk.Frame(outer, bg=BG)
hdr.pack(fill=tk.X, pady=(0, 6))

logo_c = tk.Canvas(hdr, width=26, height=26, bg=BG, highlightthickness=0)
logo_c.pack(side=tk.LEFT, padx=(0, 8))
logo_c.create_rectangle(0,  0, 11, 11, fill=ACCENT,  outline="")
logo_c.create_rectangle(15, 0, 26, 11, fill=BTN_MID, outline="")
logo_c.create_rectangle(0, 15, 11, 26, fill=BTN_MID, outline="")
logo_c.create_rectangle(15,15, 26, 26, fill=ACCENT,  outline="")

tk.Label(hdr, text="TESSERA", font=("Segoe UI", 18, "bold"),
         bg=BG, fg=LIGHT).pack(side=tk.LEFT)

tk.Label(outer, text="Secure password generator — crafted for the cautious.",
         font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(anchor="w", pady=(0, 10))

# ── Main card 
card = tk.Frame(outer, bg=CARD, padx=20, pady=16)
card.pack(fill=tk.X)

# ── Length 
tk.Label(card, text="PASSWORD LENGTH", font=("Segoe UI", 7, "bold"),
         bg=CARD, fg=MUTED).pack(anchor="w")

len_row = tk.Frame(card, bg=CARD)
len_row.pack(fill=tk.X, pady=(3, 8))

len_var = tk.StringVar(value="20")

length_scale = ttk.Scale(len_row, from_=4, to=64, orient="horizontal",
                          style="T.Horizontal.TScale", command=on_scale)
length_scale.set(20)
length_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

len_entry = tk.Entry(len_row, textvariable=len_var, width=4,
                     font=("Segoe UI", 11), bg=FIELD, fg=LIGHT,
                     insertbackground=LIGHT, relief="flat", justify="center",
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT)
len_entry.pack(side=tk.LEFT)
len_var.trace_add("write", on_entry_change)

tk.Frame(card, bg=BORDER, height=1).pack(fill=tk.X, pady=(0, 8))

# ── Character types 
tk.Label(card, text="CHARACTER TYPES", font=("Segoe UI", 7, "bold"),
         bg=CARD, fg=MUTED).pack(anchor="w", pady=(0, 4))

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
num_var   = tk.BooleanVar(value=True)
sym_var   = tk.BooleanVar(value=True)
excl_var  = tk.BooleanVar(value=False)

char_vars_list[:] = [upper_var, lower_var, num_var, sym_var]

chk_frame = tk.Frame(card, bg=CARD)
chk_frame.pack(anchor="w")

for txt, var in [
    ("Uppercase letters (A–Z)",            upper_var),
    ("Lowercase letters (a–z)",            lower_var),
    ("Numbers (0–9)",                      num_var),
    ("Symbols (!@#$…)",                    sym_var),
    ("Exclude similar characters (O, 0, l, I, 1)", excl_var),
]:
    tk.Checkbutton(chk_frame, text=txt, variable=var,
                   bg=CARD, fg=LIGHT, activebackground=CARD,
                   activeforeground=LIGHT, selectcolor=FIELD,
                   font=("Segoe UI", 9)).pack(anchor="w")

for v in char_vars_list:
    v.trace_add("write", sync_sel_btn)

sel_btn = tk.Button(card, text="Deselect All", font=("Segoe UI", 8),
                    bg=FIELD, fg=MUTED, activebackground=BORDER,
                    relief="flat", padx=8, pady=2, cursor="hand2",
                    command=toggle_all)
sel_btn.pack(anchor="w", pady=(4, 0))

tk.Frame(card, bg=BORDER, height=1).pack(fill=tk.X, pady=8)

# ── Generate button 
generate_btn = tk.Button(card, text="Generate Password",
                         font=("Segoe UI", 10, "bold"),
                         bg=BTN_MID, fg=LIGHT, relief="flat",
                         pady=8, cursor="hand2",
                         activebackground=ACCENT, command=generate)
generate_btn.pack(fill=tk.X, pady=(0, 4))

# ── Status 
status_lbl = tk.Label(card, text="", font=("Segoe UI", 8),
                      bg=CARD, fg=ERR)
status_lbl.pack()

# ── Password display 
pw_field = tk.Frame(card, bg=FIELD,
                    highlightthickness=1, highlightbackground=BORDER)
pw_field.pack(fill=tk.X, pady=(2, 4))

pw_var = tk.StringVar()
pw_entry = tk.Entry(pw_field, textvariable=pw_var,
                    font=("Consolas", 12, "bold"), justify="center",
                    bg=FIELD, fg=MUTED, relief="flat",
                    state="readonly", readonlybackground=FIELD)
pw_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=9)

eye_var = tk.BooleanVar(value=True)
toggle_eye = tk.Button(pw_field, text="🙈", font=("Segoe UI", 10),
                       bg=FIELD, fg=BORDER, relief="flat", bd=0,
                       activebackground=FIELD, state="disabled",
                       cursor="hand2", command=toggle_eye_fn)
toggle_eye.pack(side=tk.RIGHT, padx=8)

refresh_display()

# ── Copy button 
copy_btn = tk.Button(card, text="Copy Password",
                     font=("Segoe UI", 10, "bold"),
                     bg=CARD, fg=MUTED, relief="flat",
                     pady=8, cursor="hand2",
                     activebackground=BTN_MID,
                     command=copy_pw)
copy_btn.pack(fill=tk.X, pady=(0, 4))
set_copy(False)

# ── Strength bar 
strength_lbl = tk.Label(card, text="Strength:", font=("Segoe UI", 9, "bold"),
                         bg=CARD, fg=ACCENT, anchor="w")
strength_lbl.pack(fill=tk.X, pady=(2, 2))

BAR_W, BAR_H = 400, 5
bar_bg = tk.Frame(card, bg=BORDER, height=BAR_H)
bar_bg.pack(fill=tk.X)
bar_bg.pack_propagate(False)

strength_cv = tk.Canvas(bar_bg, height=BAR_H, bg=BORDER, highlightthickness=0)
strength_cv.pack(fill=tk.X)

def on_bar_resize(_e):
    if current_password:
        update_strength(current_password)
strength_cv.bind("<Configure>", on_bar_resize)

# ── History 
tk.Frame(outer, bg=BG, height=10).pack()

hist_hdr = tk.Frame(outer, bg=BG)
hist_hdr.pack(fill=tk.X)
tk.Label(hist_hdr, text="RECENT PASSWORDS",
         font=("Segoe UI", 7, "bold"), bg=BG, fg=MUTED).pack(side=tk.LEFT)
tk.Label(hist_hdr, text="Click a password to reveal",
         font=("Segoe UI", 7), bg=BG, fg=MUTED).pack(side=tk.RIGHT)

hist_card = tk.Frame(outer, bg=CARD, padx=10, pady=6)
hist_card.pack(fill=tk.X, pady=(3, 0))
hist_card.config(height=110)
hist_card.pack_propagate(False)

hist_inner = tk.Frame(hist_card, bg=CARD)
hist_inner.pack(fill=tk.BOTH, expand=True)

draw_history()

_is_fullscreen = False
_normal_geo    = ""

def toggle_fullscreen(_e=None):
    global _is_fullscreen, _normal_geo
    _is_fullscreen = not _is_fullscreen
    if _is_fullscreen:
        _normal_geo = root.geometry()
        root.attributes("-fullscreen", True)
        fs_btn.config(text="⛶  Exit Fullscreen")
    else:
        root.attributes("-fullscreen", False)
        root.geometry(_normal_geo)
        fs_btn.config(text="⛶  Fullscreen")

def exit_fullscreen(_e=None):
    global _is_fullscreen, _normal_geo
    if _is_fullscreen:
        _is_fullscreen = False
        root.attributes("-fullscreen", False)
        root.geometry(_normal_geo)
        fs_btn.config(text="⛶  Fullscreen")

fs_btn = tk.Button(hdr, text="⛶  Fullscreen",
                   font=("Segoe UI", 8), bg=BG, fg=MUTED,
                   activebackground=BORDER, activeforeground=LIGHT,
                   relief="flat", padx=6, pady=2, cursor="hand2",
                   command=toggle_fullscreen)
fs_btn.pack(side=tk.RIGHT)

# ── Keyboard shortcuts 
root.bind("<Return>",  generate)
root.bind("<F11>",     toggle_fullscreen)
root.bind("<Escape>",  exit_fullscreen)

root.update_idletasks()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

if __name__ == "__main__":
    root.mainloop()