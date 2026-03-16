import customtkinter as ctk
from tkinter import messagebox
import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SettingsManager:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Settings Manager")
        self.app.geometry("800x600")

        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main()

    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(self.app, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(sidebar, text="Settings Manager",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        ctk.CTkLabel(sidebar, text="Theme:", font=ctk.CTkFont(size=14)).pack(pady=10)

        btn_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Jasny",
                      command=lambda: ctk.set_appearance_mode("light"),
                      width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Ciemny",
                      command=lambda: ctk.set_appearance_mode("dark"),
                      width=80).pack(side="left", padx=5)

    def setup_main(self):
        main = ctk.CTkFrame(self.app, corner_radius=10)
        main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(main, text="Main Settings",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        self.entry = ctk.CTkEntry(main, placeholder_text="Enter username...",
                                  width=300, height=35)
        self.entry.pack(pady=10)

        self.check_var = ctk.BooleanVar()
        ctk.CTkCheckBox(main, text="Remember settings",
                        variable=self.check_var).pack(pady=10)

        ctk.CTkButton(main, text="Save Settings",
                      command=self.save_settings,
                      height=40).pack(pady=20)

        frame = ctk.CTkFrame(main)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Recent Activities:",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=10)

        self.textbox = ctk.CTkTextbox(frame, height=150)
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Przykładowe dane
        for item in ["App started", "Theme: Dark", "Ready"]:
            self.textbox.insert("end", f"✓ {item}\n")

    def save_settings(self):
        if self.entry.get():
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.textbox.insert("0.0", f"[{timestamp}] Saved: {self.entry.get()}\n")
            self.entry.delete(0, "end")
            self.check_var.set(False)
        else:
            messagebox.showwarning("Warning", "Enter username!")

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    SettingsManager().run()