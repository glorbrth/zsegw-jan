import tkinter as tk
from tkinter import ttk
import threading

def show_selection(event):
    """Funkcja obsługująca zdarzenie wyboru w Combobox."""
    print(f"Wybrano opcję: {combo.get()}")

def start_progress():
    """Funkcja symulująca i sterująca paskiem postępu."""
    # Uruchomienie paska w trybie indeterministycznym
    pbar.start(15) # 10 to interwał w milisekundach
    t = threading.Thread(stop_after())
    t.start()
    
def stop_after():
    root.after(3000,pbar.stop)
    
root = tk.Tk()
root.title("Ustawienia Systemu")

# --- 1. Notebook (Karty) ---
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill="both")

# Tworzenie ramek na karty
tab1 = ttk.Frame(notebook, padding="10")
tab2 = ttk.Frame(notebook, padding="10")

# Dodawanie kart do Notebook
notebook.add(tab1, text="Karta 1: Wygląd")
notebook.add(tab2, text="Karta 2: Prywatność")

# --- Zawartość Karty 1 (Combobox) ---
ttk.Label(tab1, text="Wybierz motyw:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

motywy = ["Jasny", "Ciemny", "Systemowy"]
combo = ttk.Combobox(tab1, values=motywy, state="readonly")
combo.current(0) # Ustawienie domyślnej wartości
combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Przypisanie zdarzenia <<ComboboxSelected>>
combo.bind("<<ComboboxSelected>>", show_selection)

boxVal = tk.BooleanVar()
chbox = ttk.Checkbutton(tab1,text="Włącz wysoki kontrast",variable=boxVal)
chbox.grid(row=1,column=0,padx=5, pady=5, sticky="ew")

# --- Zawartość Karty 2 ---
selected = tk.StringVar()
r1 = ttk.Radiobutton(tab2,text="Wszystkie",value="Wszystkie",variable=selected)
r1.grid(row=0,column=0,padx=5, pady=5, sticky="ew")
r2 = ttk.Radiobutton(tab2,text="Anonimowe",value="Anonimowe",variable=selected)
r2.grid(row=1,column=0,padx=5, pady=5, sticky="ew")
r3 = ttk.Radiobutton(tab2,text="Żadne",value="Żadne",variable=selected)
r3.grid(row=2,column=0,padx=5, pady=5, sticky="ew")

# --- Progress bar --

pbar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
pbar.pack(pady=10)

ttk.Button(root, text="Start Procesu", command=start_progress).pack(side="left", padx=5)


root.mainloop()
            