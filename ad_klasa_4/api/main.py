import customtkinter as ctk
import requests as reqs

def przelicz():
    resp = reqs.get("http://api.nbp.pl/api/exchangerates/tables/A/?format=json")
    data = resp.json()
    waluty = data[0]["rates"]
    kurs = [x['mid'] for x in waluty if x['code'] == str(opts.get())][0]
    pln = float(pln_entry.get())
    out.configure(text=f"moje obliczenia: {round(pln/kurs,2)}")
    edate = data[0]["effectiveDate"]
    date.configure(text=str(edate))

# Globalne ustawienia motywu
ctk.set_appearance_mode("dark")  # Opcje: "System", "Dark", "Light"
ctk.set_default_color_theme("blue") # Akcenty: "blue", "green", "dark-blue"

app = ctk.CTk()
app.title("Przelicznik")

pln_entry = ctk.CTkEntry(app, width=100, height=40)
pln_entry.pack(pady=20)

resp = reqs.get("http://api.nbp.pl/api/exchangerates/tables/A/?format=json")
data = resp.json()
waluty = data[0]["rates"]
lista_walut = [x['code'] for x in waluty]

opts = ctk.CTkOptionMenu(app, values=lista_walut)
opts.pack(pady=20)

# Dodanie nowoczesnego przycisku
btn = ctk.CTkButton(app, text="Przelicz",command=przelicz)
btn.pack(pady=20)

out = ctk.CTkLabel(app, text="")
out.pack(pady=20)

date = ctk.CTkLabel(app, text="")
date.pack(pady=20)

app.mainloop()
