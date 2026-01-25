import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import queue
import time

# --- MODEL (Zarządzanie danymi i wątkami) ---
class DBModel:
    def __init__(self):
        self.db_name = "rezerwacje.db"
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS wizyty (klient TEXT, telefon NUMBER)")

    def save_to_db_worker(self, name, number, result_queue):
        """Metoda wykonywana w osobnym wątku (Worker)"""
        try:
            # Symulacja ciężkiej pracy (np. walidacja w zewnętrznym API)
            time.sleep(2) 
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO wizyty VALUES (?, ?)", (name,number))
                conn.commit()
            result_queue.put(("SUCCESS", f"Zapisano wizytę: {name} : {number}"))
        except Exception as e:
            result_queue.put(("ERROR", str(e)))

# --- VIEW & CONTROLLER ---
class App(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.title("MVC Tkinter - System Rezerwacji")
        self.geometry("300x200")
        self.result_queue = queue.Queue()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Imię i Nazwisko:").pack(pady=5)
        self.entry_name = tk.Entry(self)
        self.entry_name.pack(pady=5)

        tk.Label(self, text="Telefon:").pack(pady=5)
        self.entry_telefon = tk.Entry(self)
        self.entry_telefon.pack(pady=5)

        self.btn_save = tk.Button(self, text="Zarezerwuj", command=self.handle_save)
        self.btn_save.pack(pady=10)

        self.status_label = tk.Label(self, text="Status: Gotowy", fg="blue")
        self.status_label.pack(pady=5)

    def handle_save(self):
        name = self.entry_name.get()
        number = self.entry_telefon.get()
        if not name:
            messagebox.showwarning("Błąd", "Wpisz nazwisko!")
            return
        if not number:
            messagebox.showwarning("Błąd", "Wpisz telefon!")
            return

        self.btn_save.config(state="disabled")
        self.status_label.config(text="Zapisywanie w tle...")

        # URUCHOMIENIE WĄTKU (Model pracuje w tle)
        thread = threading.Thread(target=self.model.save_to_db_worker, args=(name, number, self.result_queue))
        thread.start()

        # ROZPOCZĘCIE SPRAWDZANIA KOLEJKI (Odpowiednik nasłuchiwania w EDT)
        self.check_queue()

    def check_queue(self):
        """Sprawdza czy wątek tła wrzucił coś do kolejki"""
        try:
            msg_type, message = self.result_queue.get_nowait()
            # Jeśli tu dotarliśmy, dane są gotowe
            self.status_label.config(text=f"Status: {message}")
            self.btn_save.config(state="normal")
            self.entry_name.delete(0, tk.END)
            self.entry_telefon.delete(0, tk.END)
        except queue.Empty:
            # Jeśli kolejka pusta, sprawdź ponownie za 100ms
            self.after(100, self.check_queue)

if __name__ == "__main__":
    model = DBModel()
    app = App(model)
    app.mainloop()