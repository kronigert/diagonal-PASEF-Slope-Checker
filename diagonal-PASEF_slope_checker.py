import sys
import os
import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# GUI Setup
app = TkinterDnD.Tk()
app.title("diagonal-PASEF Slope Checker v0.1.1")
app.geometry("900x700")
app.configure(bg="#E4EFF7")
app.iconbitmap(resource_path("logo.ico"))

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Globals
file_path = None
lines = []
canvas_widget = None

# Helpers
def calculate_slope(y1, x1, y2, x2):
    try:
        return (float(y2) - float(y1)) / (float(x2) - float(x1))
    except ZeroDivisionError:
        return None

def process_file(path):
    output_textbox.delete('1.0', 'end')
    global file_path, lines
    file_path = path
    with open(path, 'r') as f:
        lines = f.readlines()
    output_textbox.insert("end", f"Loaded: {os.path.basename(path)}\n")
    check_slopes()

def load_file():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        process_file(path)
    else:
        output_textbox.insert("end", "No file selected.\n")

# Check Logic
def check_slopes():
    global canvas_widget
    if not lines:
        output_textbox.insert("end", "Please load a file first.\n")
        return
    slopes = []
    cycle = 0
    differing_cycles = []
    ref_slope = None

    for L in lines[2:]:
        if L.startswith("#"):
            break
        parts = L.strip().split(',')
        if len(parts) >= 6:
            cycle += 1
            s = calculate_slope(parts[1].strip(), parts[2].strip(), parts[4].strip(), parts[5].strip())
            if s is not None:
                if ref_slope is None:
                    ref_slope = s
                elif abs(s - ref_slope) > 1e-9:
                    differing_cycles.append(cycle)
                slopes.append((cycle, s))

    output_textbox.insert("end", f"Slopes found: {[s for _, s in slopes]}\n")
    if len(slopes) < 2:
        output_textbox.insert("end", "Not enough valid slopes to compare.\n")
        return
    if not differing_cycles:
        output_textbox.insert("end", "All slopes identical.\n")
    else:
        output_textbox.insert("end", f"Slopes differ at cycles: {differing_cycles}\n")
 
# Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

# Plotting
    fig = Figure(figsize=(6, 3), dpi=100)
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    for cycle, slope in slopes:
        parts = lines[cycle + 1].strip().split(',')
        y1, x1, y2, x2 = float(parts[1].strip()), float(parts[2].strip()), float(parts[4].strip()), float(parts[5].strip())
        color = 'g' if abs(slope - ref_slope) <= 1e-9 else 'r'
        ax.plot([x1, x2], [y1, y2], color=color, marker='o')
    ax.set_title("Slope Visualization")
    ax.set_xlabel("m/z")
    ax.set_ylabel("1/k0")
    ax.grid(True)

    canvas_widget = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill="both", expand=True)

# Adapt Logic
def adapt_slopes():
    global canvas_widget
    if not lines:
        output_textbox.insert("end", "Please load a file first.\n")
        return
    entries = []
    cycle = 0
    for L in lines[2:]:
        if L.startswith("#"): break
        raw = L.rstrip('\n')
        parts = raw.split(',')
        if len(parts) >= 6:
            cycle += 1
            y1, x1, y2, x2 = parts[1].strip(), parts[2].strip(), parts[4].strip(), parts[5].strip()
            s = calculate_slope(y1, x1, y2, x2)
            if s is not None:
                entries.append((cycle, s, raw))
    if len(entries) < 2:
        output_textbox.insert("end", "Not enough valid slopes to adapt.\n")
        return
    _, ref_slope, _ = entries[0]
    new_lines = lines[:2]
    adaptations = []
    idx = 0
    for L in lines[2:]:
        if L.startswith("#"):
            new_lines.append(L)
            continue
        if idx < len(entries):
            cyc, slope, orig_raw = entries[idx]
            parts = orig_raw.split(',')
            orig_x2_str = parts[5]
            orig_x2 = float(parts[5].strip())
            if abs(slope - ref_slope) > 0:
                y1, x1, y2 = float(parts[1].strip()), float(parts[2].strip()), float(parts[4].strip())
                new_x2 = x1 + (y2 - y1) / ref_slope
                prefix = orig_x2_str[:len(orig_x2_str) - len(orig_x2_str.lstrip())]
                new_sub = prefix + f"{new_x2:.1f}"
                if abs(new_x2 - orig_x2) > 1e-9:
                    new_line = orig_raw.replace(orig_x2_str, new_sub, 1)
                    adaptations.append((cyc, orig_raw, new_line))
                    new_lines.append(new_line + '\n')
                else:
                    new_lines.append(L)
            else:
                new_lines.append(L)
            idx += 1
        else:
            new_lines.append(L)
    out_path = file_path.replace(".txt", "_modified.txt")
    with open(out_path, 'w') as f:
        f.writelines(new_lines)
    output_textbox.insert("end", f"Saved adapted file as {os.path.basename(out_path)}\n")
    if adaptations:
        output_textbox.insert("end", "Adaptations made:\n")
        for cyc, orig, new in adaptations:
            output_textbox.insert("end", f"  - Cycle {cyc}:\n")
            output_textbox.insert("end", f"    Original: {orig}\n")
            output_textbox.insert("end", f"    Adapted:  {new}\n")
    else:
        output_textbox.insert("end", "No adaptations were necessary.\n")

    # Update plot with adapted slopes
    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6, 3), dpi=100)
    fig.subplots_adjust(bottom=0.2)  # Increase bottom margin
    ax = fig.add_subplot(111)
    for cyc, _, _ in entries:
        parts = lines[cyc + 1].strip().split(',')
        y1, x1, y2, x2 = float(parts[1].strip()), float(parts[2].strip()), float(parts[4].strip()), float(parts[5].strip())
        ax.plot([x1, x2], [y1, y2], color='g', marker='o')
    ax.set_title("Adapted Slope Visualization")
    ax.set_xlabel("m/z")
    ax.set_ylabel("1/k0")
    ax.grid(True)

    canvas_widget = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill="both", expand=True)

# Drag & Drop
def drop_event(event):
    path = event.data.strip("{}")
    if os.path.isfile(path) and path.lower().endswith(".txt"):
        process_file(path)
    else:
        output_textbox.insert("end", "Unsupported drop – please drop a .txt file.\n")

# Toolbar frame
btn_frame = ctk.CTkFrame(app, fg_color="#E4EFF7")
btn_frame.pack(fill="x", pady=(10, 0), padx=20)

# Buttons
for idx, (txt, cmd) in enumerate([
    ("Load .txt", load_file),
    ("Adapt", adapt_slopes)
]):
    btn = ctk.CTkButton(
        btn_frame, text=txt, command=cmd,
        fg_color="#0071BC", hover_color="#004E82",
        text_color="white", corner_radius=8,
        width=120, height=36
    )
    btn.grid(row=0, column=idx, padx=10, pady=5)

# Title and GitHub link
title_label = ctk.CTkLabel(
    btn_frame,
    text="diagonal-PASEF Slope Checker v0.1.1",
    text_color="#004E82",
    font=("Arial", 16, "bold")
)
title_label.grid(row=0, column=2, padx=(30, 10), sticky="e")

link_label = ctk.CTkLabel(
    btn_frame,
    text="GitHub",
    text_color="#004E82",
    font=("Arial", 14, "bold"),
    cursor="hand2"
)
link_label.grid(row=0, column=3, padx=(175, 10))
link_label.bind("<Button-1>", lambda e: os.system("start https://github.com/kronigert/diagonal-PASEF_slope_checker/"))



# Separator
separator = ctk.CTkFrame(app, height=2, fg_color="#004E82")
separator.pack(fill="x", padx=20, pady=(0,10))

# Output Textbox
output_textbox = ctk.CTkTextbox(
    app, width=860, height=200, corner_radius=10,
    fg_color="white", text_color="#04304D", font=("Courier",12)
)
output_textbox.pack(padx=20, pady=10, fill="both", expand=True)
output_textbox.drop_target_register(DND_FILES)
output_textbox.dnd_bind('<<Drop>>', drop_event)

# Plot Frame
plot_frame = ctk.CTkFrame(app, fg_color="white")
plot_frame.pack(padx=20, pady=10, fill="both", expand=True)

app.mainloop()
