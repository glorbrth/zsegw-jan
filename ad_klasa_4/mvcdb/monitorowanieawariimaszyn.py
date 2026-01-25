import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import queue
import time

# --- MODEL (Zarządzanie danymi i wątkami) ---
class MaintenanceModel:
    def __init__(self):
        self.db_name = "maintenance.db"
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS incidents (id INTEGER AUTO_INCREMENT PRIMARY KEY, nr_maszyny TEXT, opis TEXT, oczekiwany_czas_naprawy TEXT);")

    def save_to_db_worker(self, nr_maszyny, opis, oczekiwany_czas_naprawy, result_queue):
        """Metoda wykonywana w osobnym wątku (Worker)"""
        try:
            print(nr_maszyny)
            print(opis)
            print(oczekiwany_czas_naprawy)
            # Symulacja ciężkiej pracy (np. walidacja w zewnętrznym API)
            time.sleep(3) 
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO incidents(`nr_maszyny`,`opis`,`oczekiwany_czas_naprawy`) VALUES (?, ?, ?);", (nr_maszyny, opis, oczekiwany_czas_naprawy))
                conn.commit()
            result_queue.put(("SUCCESS", f"Zgłoszono incydent: \n nr_maszyny: {nr_maszyny} \n opis: {opis} \n {oczekiwany_czas_naprawy}"))
        except Exception as e:
            result_queue.put(("ERROR", str(e)))

class App(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.title("System Monitorowania Awarii Maszyn")
        self.geometry("500x350")
        self.result_queue = queue.Queue()
        self.setup_ui()

    def setup_ui(self):
        options_list = ["M1", "M2", "M3"]
        self.wybrano = tk.StringVar(self)
        self.opcje = tk.OptionMenu(self,self.wybrano,*options_list)
        self.opcje.pack(pady=10)

        self.opisLbl = tk.Label(self,text="Opis:")
        self.opisLbl.pack(pady=0)

        self.opis = tk.Text(self,height=4,width=40)
        self.opis.pack(pady=10)

        self.czasLbl = tk.Label(self,text="Oczekiwany czas naprawy:")
        self.czasLbl.pack(pady=10)

        self.czas = tk.Entry(self)
        self.czas.pack()

        self.btn_save = tk.Button(self, text="Zarezerwuj", command=self.handle_save)
        self.btn_save.pack(pady=10)

        self.status_label = tk.Label(self, text="Status: Gotowy", fg="blue")
        self.status_label.pack(pady=5)

    def handle_save(self):
        opcja = self.wybrano.get()
        opis = self.opis.get('1.0',tk.END)
        czas = self.czas.get()
        if (not opcja) or (not opis) or (not czas):
            messagebox.showwarning("Błąd", "Wypełnij wszystkie pola")
            return

        self.btn_save.config(state="disabled")
        self.status_label.config(text="TRWA PRZESYŁANIE DANYCH...",fg="red")

        # URUCHOMIENIE WĄTKU (Model pracuje w tle)
        thread = threading.Thread(target=self.model.save_to_db_worker, args=(opcja,opis,czas,self.result_queue))
        thread.start()

        # ROZPOCZĘCIE SPRAWDZANIA KOLEJKI (Odpowiednik nasłuchiwania w EDT)
        self.check_queue()

    def check_queue(self):
        """Sprawdza czy wątek tła wrzucił coś do kolejki"""
        try:
            msg_type, message = self.result_queue.get_nowait()
            # Jeśli tu dotarliśmy, dane są gotowe
            self.status_label.config(text=f"Status: {message}",fg="blue")
            self.btn_save.config(state="normal")
        except queue.Empty:
            # Jeśli kolejka pusta, sprawdź ponownie za 100ms
            self.after(100, self.check_queue)

if __name__ == "__main__":
    model = MaintenanceModel()
    app = App(model)
    app.mainloop()