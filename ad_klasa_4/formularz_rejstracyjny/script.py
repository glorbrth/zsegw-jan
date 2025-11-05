
import tkinter as tk
from tkinter import messagebox

def submit_form():
    # Pobieranie danych z Entry
    imie = pole_imie.get()
    email = pole_email.get()
    wiek = stan_wiek.get()
    ksiazki = "ksiazki" if stan_ksiazki.get() else ""
    sport = "sport" if stan_sport.get() else ""
    uwagi = text_uwagi.get(1.0,"end")
    
    komunikat = f"Imię: {imie}\nEmail: {email}\nWiek: {wiek}\nZainteresowania: {ksiazki}  {sport}\nUwagi: {uwagi}"
    
    # Wyświetlenie komunikatu w oknie dialogowym
    messagebox.showinfo("Podsumowanie", komunikat)



# 1. Inicjalizacja głównego okna
root = tk.Tk()
root.title("Formularz Rejstracyjny")
root.geometry("400x700")

stan_wiek = tk.StringVar(value="18-30") # Ustawienie domyślnej wartości
stan_ksiazki = tk.IntVar()
stan_sport = tk.IntVar()

tk.Label(root, text="Podaj Imię:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
pole_imie = tk.Entry(root, width=30)
pole_imie.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Podaj Email:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
pole_email = tk.Entry(root, width=30)
pole_email.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Podaj Wiek (Kategoria):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
tk.Radiobutton(root, text="18-30", variable=stan_wiek, value="18-30").grid(row=3, column=0, sticky="w", padx=20)
tk.Radiobutton(root, text="31-50", variable=stan_wiek, value="31-50").grid(row=4, column=0, sticky="w", padx=20)
tk.Radiobutton(root, text="50+", variable=stan_wiek, value="50+").grid(row=5, column=0, sticky="w", padx=20)

tk.Label(root, text="Zainteresowania: ").grid(row=6, column=0, padx=10, pady=10, sticky="w")
przycisk_ksiazki = tk.Checkbutton(root, text="Ksiażki", variable=stan_ksiazki)
przycisk_ksiazki.grid(row=6, column=1, columnspan=2, pady=5, sticky="w")
przycisk_sport = tk.Checkbutton(root, text="Sport", variable=stan_sport)
przycisk_sport.grid(row=7, column=1, columnspan=2, pady=5, sticky="w")

tk.Label(root, text="Uwagi: ").grid(row=8, column=0, padx=10, pady=10, sticky="w")
text_uwagi = tk.Text(root,height=4,width=45)
text_uwagi.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Button
przycisk_akcja = tk.Button(root, text="Zarejstruj", command=submit_form, bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'))
przycisk_akcja.grid(row=10, column=0, columnspan=2, pady=20)


# Uruchomienie pętli głównej
root.mainloop()
    