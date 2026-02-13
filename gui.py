import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

# ---------- CONFIGURATION ----------
BG_COLOR = "#f0f4f8"       # light, calm blue-gray background
FG_COLOR = "#333333"       # dark text for readability
BUTTON_BG = "#4a90e2"      # bright blue button background
BUTTON_FG = "#ffffff"      # white button text
OUTPUT_BG = "#ffffff"      # white output background
OUTPUT_FG = "#222222"      # dark text for output
ERROR_COLOR = "#d9534f"    # bootstrap-style red for errors
FONT = ("Consolas", 11)
HEADER_FONT = ("Helvetica", 20, "bold")

# ---------- RUN CHECKER ----------
def run_checker():
    file_path = filedialog.askopenfilename(filetypes=[
        ("C files", "*.c"),
        ("C++ files", "*.cpp"),
        ("Text files", "*.txt"),
        ("All files", ".")
    ])
    
    if not file_path:
        return

    output_text.config(state=tk.NORMAL)  # Enable editing to update text
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"> Checking syntax for:\n{file_path}\n\n")

    try:
        result = subprocess.run(
            ['CSyntaxChecker.exe', file_path],
            capture_output=True,
            text=True
        )

        # Normal output
        if result.stdout:
            output_text.insert(tk.END, "✔ Output:\n" + result.stdout + "\n")

        # Highlight errors in red
        if result.stderr:
            start_index = output_text.index(tk.END)
            output_text.insert(tk.END, "⚠ Errors:\n" + result.stderr)
            end_index = output_text.index(tk.END)
            output_text.tag_add("error", start_index, end_index)

        output_text.config(state=tk.DISABLED)  # Make text read-only

    except FileNotFoundError:
        messagebox.showerror("Error", "CSyntaxChecker.exe not found. Did you compile it?")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("C Syntax Checker")
root.configure(bg=BG_COLOR)
root.geometry("820x600")
root.resizable(False, False)

# Header
header = tk.Label(
    root,
    text="C Syntax Checker GUI",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=HEADER_FONT
)
header.pack(pady=20)

# Button
check_button = tk.Button(
    root,
    text="Select File and Check Syntax",
    command=run_checker,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground="#357ABD",
    font=("Helvetica", 14, "bold"),
    padx=15,
    pady=8,
    relief=tk.FLAT,
    cursor="hand2"
)
check_button.pack(pady=10)

# Output frame
output_frame = tk.Frame(root, bg=BG_COLOR)
output_frame.pack(pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(
    output_frame,
    wrap=tk.WORD,
    yscrollcommand=scrollbar.set,
    font=FONT,
    bg=OUTPUT_BG,
    fg=OUTPUT_FG,
    insertbackground=FG_COLOR,
    relief=tk.SOLID,
    borderwidth=1
)
output_text.pack(fill="both", expand=True)
scrollbar.config(command=output_text.yview)

# Error tag config
output_text.tag_config("error", foreground=ERROR_COLOR, font=("Consolas", 11, "bold"))

# Start GUI loop
root.mainloop()