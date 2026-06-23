import tkinter as tk
from tkinter import messagebox

class SetupDialog:
    def __init__(self, parent, on_submit_callback):
        self.parent = parent
        self.on_submit_callback = on_submit_callback
        self.setup_inputs = {}
        
        self.setup_frame = tk.Frame(parent, bg="#1E1E1E")
        self.setup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(self.setup_frame, text="Define Domain Size", bg="#1E1E1E", fg="white", font=('Arial', 24, 'bold')).pack(pady=25)
        
        inputs_frame = tk.Frame(self.setup_frame, bg="#1E1E1E")
        inputs_frame.pack(pady=10)
        
        for lbl, key in [("Length X (Lx):", "Lx"), ("Length Y (Ly):", "Ly"), ("Length Z (Lz):", "Lz")]:
            f = tk.Frame(inputs_frame, bg="#1E1E1E")
            f.pack(fill=tk.X, pady=10)
            tk.Label(f, text=lbl, bg="#1E1E1E", fg="white", width=15, anchor="w", font=('Arial', 14)).pack(side=tk.LEFT)
            e = tk.Entry(f, width=15, bg="#404040", fg="white", insertbackground="white", relief="flat", font=('Arial', 14))
            e.insert(0, "1.0")
            e.pack(side=tk.RIGHT, padx=10)
            self.setup_inputs[key] = e
            
        tk.Button(self.setup_frame, text="Create Environment", bg="#006400", fg="white", font=('Arial', 14, 'bold'), relief="flat", command=self.on_submit, padx=20, pady=10).pack(pady=40)
        
    def on_submit(self):
        try:
            Lx = float(self.setup_inputs["Lx"].get())
            Ly = float(self.setup_inputs["Ly"].get())
            Lz = float(self.setup_inputs["Lz"].get())
            if Lx <= 0 or Ly <= 0 or Lz <= 0:
                raise ValueError("Dimensions must be positive!")
                
            self.setup_frame.place_forget()
            self.on_submit_callback(Lx, Ly, Lz)
        except ValueError:
            messagebox.showerror("Error", "Invalid dimensions! Please enter positive numbers.")
