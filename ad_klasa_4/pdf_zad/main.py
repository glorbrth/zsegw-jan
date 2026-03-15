import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def generuj_pdf():
    # 1. Pobieranie danych z interfejsu
    imie = entry_imie.get()
    notatka = text_notatka.get("1.0", tk.END).strip()
    nazwa = entry_nazwa.get()
    cena = int(entry_netto.get())
    vat = int(entry_vat.get())

    stawka = (cena * vat)/100
    brutto = cena+vat

    if not imie or not notatka or not nazwa or not cena or not vat:
        messagebox.showwarning("Błąd", "Wpisz przynajmniej imię!")
        return

    # 2. Wybór lokalizacji zapisu
    sciezka = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Pliki PDF", "*.pdf")],
        title="Zapisz raport jako..."
    )

    if sciezka:
        try:
            # 3. Tworzenie dokumentu PDF
            c = canvas.Canvas(sciezka, pagesize=A4)
            szerokosc, wysokosc = A4

            # Nagłówek
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, wysokosc - 50, "RAPORT GENEROWANY Z TKINTER")

            # Linia oddzielająca
            c.line(100, wysokosc - 60, 500, wysokosc - 60)

            # Treść
            c.setFont("Helvetica", 12)
            c.drawString(100, wysokosc - 100, f"Użytkownik: {imie}")

            c.drawString(100, wysokosc - 130, "Treść notatki:")

            # Prosta obsługa wielu linii tekstu
            tekst_obj = c.beginText(100, wysokosc - 150)
            tekst_obj.setFont("Helvetica", 10)
            tekst_obj.textLines(notatka)
            c.drawText(tekst_obj)

            data = ["Nazwa : " + nazwa,"Cena : " + str(cena),"VAT : " + str(vat) +"%", "Stawka : " + str(stawka), "Brutto : "+ str(brutto)]
            offset = 200
            for i in data:
                c.drawString(100, wysokosc-offset, i)
                offset += 15


            # Zapisanie pliku
            c.save()
            messagebox.showinfo("Sukces", "Plik PDF został utworzony pomyślnie!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")


# --- Konfiguracja Okna Tkinter ---
root = tk.Tk()
root.title("Generator PDF")
root.geometry("400x400")

tk.Label(root, text="Imię i Nazwisko:", font=("Arial", 10, "bold")).pack(pady=5)
entry_imie = tk.Entry(root, width=40)
entry_imie.pack(pady=5)

tk.Label(root, text="Treść notatki:", font=("Arial", 10, "bold")).pack(pady=5)
text_notatka = tk.Text(root, width=40, height=10)
text_notatka.pack(pady=5)

tk.Label(root, text="Nazwa produktu:", font=("Arial", 10, "bold")).pack(pady=5)
entry_nazwa = tk.Entry(root, width=40)
entry_nazwa.pack(pady=5)

tk.Label(root, text="Cena netto:", font=("Arial", 10, "bold")).pack(pady=5)
entry_netto = tk.Entry(root, width=40)
entry_netto.pack(pady=5)

tk.Label(root, text="Stawka VAT (w %):", font=("Arial", 10, "bold")).pack(pady=5)
entry_vat = tk.Entry(root, width=40)
entry_vat.pack(pady=5)

btn_export = tk.Button(root, text="Eksportuj do PDF", command=generuj_pdf, bg="#27ae60", fg="white", padx=20)
btn_export.pack(pady=20)

root.mainloop()