import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- FUNKCJE BAZY DANYCH (jak wyżej w sekcji 2) ---
# (polacz_z_baza, dodaj_dane, pobierz_wszystkie_produkty)

# --- FUNKCJE GUI ---
def polacz_z_baza():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mojabaza"
        )
        return mydb
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd Połączenia", f"Nie można połączyć się z bazą danych: {err}")
        return None

def dodaj_dane(nazwa, ilosc):
    conn = polacz_z_baza()
    if conn is None: return

    cursor = conn.cursor()
    sql = "INSERT INTO produkty (nazwa_produktu, ilosc) VALUES (%s, %s)"
    val = (nazwa, ilosc)
    try:
        cursor.execute(sql, val)
        conn.commit()
        messagebox.showinfo("Sukces", "Produkt dodany pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania: {err}")
    finally:
        cursor.close()
        conn.close()

def edytuj_dane(nazwa,nowa_nazwa,nowa_ilosc):
    conn = polacz_z_baza()
    if conn is None: return

    cursor = conn.cursor()
    sql = "UPDATE produkty SET "
    if(nowa_nazwa != ''): 
        sql+=" nazwa_produktu="+nowa_nazwa
    if(nowa_ilosc >= 0):
        sql+=" ilosc="+nowa_ilosc
    
    sql+=" WHERE nazwa_produktu="+nazwa

    try:
        cursor.execute(sql)
        conn.commit()
        messagebox.showinfo("Sukces", "Produkt dodany pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania: {err}")
    finally:
        cursor.close()
        conn.close()


def pobierz_wszystkie_produkty():
    conn = polacz_z_baza()
    if conn is None: return []

    cursor = conn.cursor()
    sql = "SELECT id, nazwa_produktu, ilosc FROM produkty"
    try:
        cursor.execute(sql)
        wyniki = cursor.fetchall() # Zwraca listę tupli
        return wyniki
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas pobierania: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def odswiez_treeview(tree):
    for item in tree.get_children():
        tree.delete(item) # Usuń stare wiersze
    dane = pobierz_wszystkie_produkty()
    for wiersz in dane:
        tree.insert('', tk.END, values=wiersz)

def obsluga_dodawania(nazwa_var, ilosc_var, tree):
    nazwa = nazwa_var.get()
    try:
        ilosc = int(ilosc_var.get())
    except ValueError:
        messagebox.showerror("Błąd", "Ilość musi być liczbą całkowitą.")
        return

    if nazwa and ilosc >= 0:
        dodaj_dane(nazwa, ilosc)
        odswiez_treeview(tree) # Odśwież widok po dodaniu
        nazwa_var.set(""); ilosc_var.set("") # Wyczyść pola
    else:
        messagebox.showwarning("Uwaga", "Wypełnij poprawnie wszystkie pola.")

def aktualizuj_ilosc(id_produktu, nowa_ilosc, tree):
    conn = polacz_z_baza()
    if conn is None: return []

    cursor = conn.cursor()
    sql = "UPDATE produkty SET ilosc = %s WHERE id = %s"
    val = (nowa_ilosc, id_produktu)
    try:
        cursor.execute(sql, val)
        conn.commit()
        messagebox.showinfo("Sukces", "Produkt zedytowany pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania: {err}")
    finally:
        odswiez_treeview(tree)
        cursor.close()
        conn.close()



# --- KONFIGURACJA GŁÓWNEGO OKNA ---

root = tk.Tk()
root.title("System Zarządzania Magazynem")

# Zmienne kontrolne dla pól wejściowych
nazwa_produktu_var = tk.StringVar()
ilosc_var = tk.StringVar()
id_produktu_var = tk.StringVar()
nowa_ilosc_var = tk.IntVar()

# --- Sekcja formularza (INPUT) ---
form_frame = ttk.Frame(root, padding="10")
form_frame.pack(padx=10, pady=10, fill='x')

ttk.Label(form_frame, text="Nazwa Produktu:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=nazwa_produktu_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Ilość:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=ilosc_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')

dodaj_btn = ttk.Button(form_frame, text="Dodaj Produkt",
    command=lambda: obsluga_dodawania(nazwa_produktu_var, ilosc_var, tree))
dodaj_btn.grid(row=2, column=0, columnspan=2, pady=10)

ttk.Label(form_frame, text="ID produktu do edycji:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=id_produktu_var, width=30).grid(row=4, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Nowa ilosc produktu:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=nowa_ilosc_var, width=10).grid(row=6, column=1, padx=5, pady=5)

edytuj_btn = ttk.Button(form_frame, text="Edytuj Produkt",
    command=lambda: aktualizuj_ilosc(id_produktu=id_produktu_var.get(),nowa_ilosc=nowa_ilosc_var.get(),tree=tree))
edytuj_btn.grid(row=7, column=0, columnspan=2, pady=10)


# --- Sekcja wyświetlania danych (Treeview) ---

columns = ('id', 'nazwa', 'ilosc')
tree = ttk.Treeview(root, columns=columns, show='headings')

tree.heading('id', text='ID')
tree.column('id', width=50, anchor='center')
tree.heading('nazwa', text='Nazwa Produktu')
tree.column('nazwa', width=250)
tree.heading('ilosc', text='Ilość')
tree.column('ilosc', width=80, anchor='center')

tree.pack(pady=10, padx=10, fill='both', expand=True)

# Początkowe załadowanie danych
odswiez_treeview(tree)

root.mainloop()