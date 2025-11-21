import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import os
from datetime import datetime
from collections import defaultdict

processed_df = None

# -------------------
# CSV Processing
# -------------------
def process_input_file(file_path):
    global processed_df

    try:
        ext = file_path.lower()

        # --- Load CSV ---
        if ext.endswith(".csv"):
            df = pd.read_csv(file_path)

        # --- Load Excel ---
        elif ext.endswith(".xlsx"):
            df = pd.read_excel(file_path)

        else:
            messagebox.showwarning("Invalid File", "File must be a CSV or Excel file.")
            return



        # Example transformation (you can change this)
        # df["Total"] = df.select_dtypes(include='number').sum(axis=1)



        processed_df = df
        save_button.config(state=tk.NORMAL)
        drop_label.config(text="File processed successfully!", bg="#d1ffd6")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file:\n{e}")


def upload_file():
    filepath = filedialog.askopenfilename(
        title="Select CSV or Excel file",
        filetypes=[
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
            ("All Supported", "*.csv *.xlsx"),
        ]
    )
    if filepath:
        process_input_file(filepath)

# -------------------
# Drag & Drop Events
# -------------------
def drop_file(event):
    filepath = event.data.strip()
    if filepath.startswith("{") and filepath.endswith("}"):
        filepath = filepath[1:-1]
    
    ext = filepath.lower()
    
    if os.path.isfile(filepath) and (ext.endswith(".csv") or ext.endswith(".xlsx")):
        process_input_file(filepath)
        drop_label.config(text="File uploaded!", bg="#d1ffd6")
    else:
        messagebox.showwarning("Invalid File", "Please drop a valid CSV file.")
    return "copy"


# -------------------
# Save Processed CSV
# -------------------
# This handler is triggered when user picks "Save as CSV"
def save_as_csv():
    if processed_df is None:
        messagebox.showwarning("Warning", "No file has been processed yet.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save as CSV"
    )
    if save_path:
        processed_df.to_csv(save_path, index=False)
        messagebox.showinfo("Saved", "File saved as CSV!")
        reset_program()


# This handler is triggered when user picks "Save as Excel"
def save_as_excel():
    if processed_df is None:
        messagebox.showwarning("Warning", "No file has been processed yet.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        title="Save as Excel"
    )
    if save_path:
        processed_df.to_excel(save_path, index=False)
        messagebox.showinfo("Saved", "File saved as Excel!")
        reset_program()

def reset_program():
    global processed_df

    processed_df = None  # clear data

    # Reset drop zone text + color
    drop_label.config(
        text="Drop CSV or Excel File Here",
        bg=drop_default_color
    )

    # Disable save button again
    save_button.config(state=tk.DISABLED)


# -------------------
# Modern UI Setup
# -------------------
root = TkinterDnD.Tk()
root.title("Proccess GIS for Water Budget")
root.geometry("600x420")
root.configure(bg="#f5f5f7")

# Modern font
font_large = ("Segoe UI", 14, "bold")
font_med = ("Segoe UI", 11)
font_small = ("Segoe UI", 10)

# Header
header = tk.Label(
    root,
    text="GIS Processor for Water Budget",
    font=font_large,
    bg="#f5f5f7",
    fg="#333"
)
header.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Upload or drag-and-drop a file to process",
    font=font_small,
    bg="#f5f5f7",
    fg="#555"
)
subtitle.pack(pady=(0, 20))


# Drop Zone (modern card look)
drop_default_color = "#ffffff"

drop_label = tk.Label(
    root,
    text="Drop CSV or Excel File Here",
    font=font_med,
    bg=drop_default_color,
    fg="#333",
    width=40,
    height=6,
    bd=0,
    relief="flat",
)

drop_label.pack(padx=2, pady=2)

drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", drop_file)

# Upload Button (modern)
upload_btn = tk.Button(
    root,
    text="Browse CSV or Excel",
    font=font_med,
    bg="#4a90e2",
    fg="white",
    activebackground="#3f7fcc",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=20,
    pady=10,
    command=upload_file
)
upload_btn.pack(pady=(20, 10))

# Save Button (modern)
# Menu for the split button
save_menu = tk.Menu(root, tearoff=0)
save_menu.add_command(label="Save as CSV", command=save_as_csv)
save_menu.add_command(label="Save as Excel", command=save_as_excel)

# Main save button
save_button = tk.Button(
    root,
    text="Save ▼",
    font=font_med,
    bg="#2ecc71",
    fg="white",
    activebackground="#27ae60",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=20,
    pady=10
)
save_button.pack(pady=(0, 10))

# When clicked, it opens the menu
def open_save_menu(event):
    save_menu.tk_popup(event.x_root, event.y_root)

save_button.bind("<Button-1>", open_save_menu)
save_button.config(state=tk.DISABLED)

root.mainloop()
