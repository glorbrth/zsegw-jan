import tkinter as tk
from tkinter import ttk

# ====================================================================
# 1. MODEL (Logika Danych)
# ====================================================================

class KwadratModel :
    """Model Danych: Przechowuje stan licznika."""
    def __init__(self):
        self._wartosc = 0

    def oblicz(self, liczba):
        self._wartosc = self._wartosc+liczba

    def get_wartosc(self):
        return self._wartosc

    def zwieksz(self):
        self._wartosc += 1

    def resetuj(self):
        self._wartosc = 0


# ====================================================================
# 2. VIEW (Interfejs Graficzny)
# ====================================================================

class LicznikView(tk.Tk):
    """Widok: Tworzy i wyświetla interfejs Tkinter."""
    def __init__(self, controller):
        super().__init__()
        self.title("Licznik MVC w Pythonie")
        self.geometry("300x150")

        self.controller = controller
        
        # Zmienna do dynamicznej aktualizacji tekstu
        self.licznik_var = tk.StringVar(value="Licznik: 0")

        self._utworz_widzety()
        
    def _utworz_widzety(self):
        """Buduje interfejs."""
        
        self.licznik_label = ttk.Label(self, textvariable=self.licznik_var, font=("Arial", 16))
        self.licznik_label.pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # Przycisk "Zwiększ": Użycie 'command' do podpięcia metody Kontrolera

        self.entry = ttk.Entry(button_frame)
        self.entry.pack(side=tk.LEFT, padx=10)

        self.zwieksz_button = ttk.Button(button_frame, text="Oblicz")
        self.zwieksz_button.config(command=self.controller.obsluz_zwieksz)
        self.zwieksz_button.pack(side=tk.LEFT, padx=10)

        # Przycisk "Resetuj"
        self.reset_button = ttk.Button(button_frame, text="Resetuj")
        self.reset_button.config(command=self.controller.obsluz_reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def ustaw_wartosc_licznika(self, nowa_wartosc):
        """Metoda wywoływana przez Kontroler do aktualizacji GUI."""
        self.licznik_var.set(f"Licznik: {nowa_wartosc}")


# ====================================================================
# 3. CONTROLLER (Pośrednik)
# ====================================================================

class LicznikController:
    """Kontroler: Koordynuje Model i View."""
    def __init__(self, model, view):
        self.model = model
        self.view = view 

    def aktualizuj_view(self):
        """Pobiera dane z Modelu i aktualizuje Widok."""
        wartosc = self.model.get_wartosc()
        self.view.ustaw_wartosc_licznika(wartosc)

    def obsluz_zwieksz(self):
        """Obsługa kliknięcia 'Zwiększ'."""
        
        self.model.oblicz(int(self.view.entry.get()))
        self.aktualizuj_view()    # Aktualizacja View

    def obsluz_reset(self):
        """Obsługa kliknięcia 'Resetuj'."""
        self.model.resetuj()      # Modyfikacja Modelu
        self.aktualizuj_view()    # Aktualizacja View

# ====================================================================
# 4. PUNKT STARTOWY
# ====================================================================

if __name__ == "__main__":
    # 1. Tworzenie Modelu
    model = KwadratModel ()

    # 2. Tworzenie Kontrolera i View (ustawienie referencji)
    # Tworzymy Controller, aby móc go przekazać do View
    controller_instance = LicznikController(model, view=None) 
    
    # Tworzymy View, przekazując mu gotowy Controller
    view_instance = LicznikView(controller_instance)
    
    # Uzupełniamy referencję View w Kontrolerze
    controller_instance.view = view_instance 
    controller_instance.aktualizuj_view()

    # 3. Uruchomienie aplikacji
    view_instance.mainloop()