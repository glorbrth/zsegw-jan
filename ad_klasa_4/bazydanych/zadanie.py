import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

''' DB:
CREATE DATABASE katalog_filmow;
CREATE TABLE filmy (
    id INT AUTO_INCREMENT,
    tytul VARCHAR(50),
    rezyser VARCHAR(50),
    rok YEAR,
    ocena INT,
    PRIMARY KEY (id)
);
'''
# --- FUNKCJE GUI ---

def polacz_z_baza():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="katalog_filmow"
        )
        return mydb
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd Połączenia", f"Nie można połączyć się z bazą danych: {err}")
        return None
    
def dodaj_dane(tytul, rezyser, rok, ocena):
    conn = polacz_z_baza()
    if conn is None: return

    cursor = conn.cursor()
    sql = "INSERT INTO filmy (tytul, rezyser, rok, ocena) VALUES (%s, %s, %s, %s)"
    val = (tytul, rezyser, rok, ocena)
    try:
        cursor.execute(sql, val)
        conn.commit()
        messagebox.showinfo("Sukces", "Film dodany pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania: {err}")
    finally:
        cursor.close()
        conn.close()

def usun_dane(id_produktu, tree):
    conn = polacz_z_baza()
    if conn is None: return

    cursor = conn.cursor()
    sql = "DELETE FROM filmy WHERE id = %s"
    val = (id_produktu,)
    try:
        cursor.execute(sql, val)
        conn.commit()
        messagebox.showinfo("Sukces", "Film usunięty pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas usuwania: {err}")
    finally:
        odswiez_treeview(tree)
        cursor.close()
        conn.close()

def pobierz_wszystkie_produkty():
    conn = polacz_z_baza()
    if conn is None: return []

    cursor = conn.cursor()
    sql = "SELECT id, tytul, rezyser, rok, ocena FROM filmy"
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

def obsluga_dodawania(tytul, rezyser, rok, ocena, tree):

    if tytul and rezyser and rok.isdigit() and ocena.isdigit():
        dodaj_dane(tytul, rezyser, rok, ocena)
        odswiez_treeview(tree)
    else:
        messagebox.showwarning("Uwaga", "Wypełnij poprawnie wszystkie pola.")

def okno_edycji(id_produktu, tytul, rezyser, rok, ocena, tree):
    popup = tk.Toplevel()
    popup.title("Edytuj Film/Serial")
    popup.geometry("300x250")
    popup.grab_set()

    tytul_var = tk.StringVar(value=tytul)
    rezyser_var = tk.StringVar(value=rezyser)
    rok_var = tk.StringVar(value=rok)
    ocena_var = tk.StringVar(value=ocena)

    popup.frame = ttk.Frame(popup, padding="10")
    popup.frame.pack(padx=10, pady=10, fill='x')

    ttk.Label(popup.frame, text="Tytuł:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    ttk.Entry(popup.frame, textvariable=tytul_var, width=30).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(popup.frame, text="Reżyser:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    ttk.Entry(popup.frame, textvariable=rezyser_var, width=30).grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(popup.frame, text="Rok:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    ttk.Entry(popup.frame, textvariable=rok_var, width=30).grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(popup.frame, text="Ocena:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
    ttk.Entry(popup.frame, textvariable=ocena_var, width=30).grid(row=3, column=1, padx=5, pady=5)

    zapisz_btn = ttk.Button(popup.frame, text="Zapisz zmiany",
        command=lambda: [aktualizuj_ilosc(id_produktu, tytul_var.get(), rezyser_var.get(), rok_var.get(), ocena_var.get(), tree), popup.destroy()])
    zapisz_btn.grid(row=4, column=0, columnspan=2, pady=10)

def aktualizuj_ilosc(id_produktu, tytul, rezyser, rok, ocena, tree):
    conn = polacz_z_baza()
    if conn is None: return []

    if not(id_produktu and tytul and rezyser and rok.isdigit() and ocena.isdigit()):
        messagebox.showwarning("Uwaga", "Wypełnij poprawnie wszystkie pola.")
        return []

    cursor = conn.cursor()
    sql = "UPDATE filmy SET tytul = %s, rezyser = %s, rok = %s, ocena = %s WHERE id = %s"
    val = (tytul, rezyser, rok, ocena, id_produktu)
    try:
        cursor.execute(sql, val)
        conn.commit()
        messagebox.showinfo("Sukces", "Produkt zedytowany pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas edytowania: {err}")
    finally:
        odswiez_treeview(tree)
        cursor.close()
        conn.close()

# --- KONFIGURACJA GŁÓWNEGO OKNA ---

root = tk.Tk()
root.title("Katalog Filmów/Seriali ")

# Zmienne kontrolne dla pól wejściowych
tytul_var = tk.StringVar()
rezyser_var = tk.StringVar()
rok_var = tk.StringVar()
ocena_var = tk.StringVar()

# --- Sekcja formularza (INPUT) ---
form_frame = ttk.Frame(root, padding="10")
form_frame.pack(padx=10, pady=10, fill='x')

ttk.Label(form_frame, text="Tytuł:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=tytul_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Reżyser:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=rezyser_var, width=30).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Rok:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=rok_var, width=30).grid(row=2, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Ocena:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=ocena_var, width=30).grid(row=3, column=1, padx=5, pady=5)

dodaj_btn = ttk.Button(form_frame, text="Dodaj Film",
    command=lambda: obsluga_dodawania(tytul_var.get(), rezyser_var.get(), rok_var.get(), ocena_var.get(), tree))
dodaj_btn.grid(row=4, column=0, columnspan=1, pady=10)

usun_btn = ttk.Button(form_frame, text="Usuń zaznaczony Film",
    command=lambda: usun_dane(tree.item(tree.selection())['values'][0], tree))
usun_btn.grid(row=4, column=1, columnspan=1, pady=10)

# --- Sekcja wyświetlania danych (Treeview) ---

columns = ('id', 'tytul', 'rezyser', 'rok', 'ocena')
tree = ttk.Treeview(root, columns=columns, show='headings')

tree.bind('<Double-1>', lambda event: okno_edycji(
    str(tree.item(tree.selection())['values'][0]),
    str(tree.item(tree.selection())['values'][1]),
    str(tree.item(tree.selection())['values'][2]),
    str(tree.item(tree.selection())['values'][3]),
    str(tree.item(tree.selection())['values'][4]),
    tree
))

tree.heading('id', text='ID')
tree.column('id', width=50, anchor='center')
tree.heading('tytul', text='Tytul_filmu')
tree.column('tytul', width=150)
tree.heading('rezyser', text='Reżyser')
tree.column('rezyser', width=100)
tree.heading('rok', text='Rok')
tree.column('rok', width=50, anchor='center')
tree.heading('ocena', text='Ocena')
tree.column('ocena', width=50, anchor='center')

tree.pack(pady=10, padx=10, fill='both', expand=True)

# Początkowe załadowanie danych
odswiez_treeview(tree)

root.mainloop()