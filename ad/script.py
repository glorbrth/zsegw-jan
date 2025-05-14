import os


class Uczen:
    def __init__(self, imie, wiek, przedmioty):
        self.imie = imie
        self.wiek = wiek
        self.przedmioty = przedmioty

    def __str__(self):
        return str(self.imie) + "   " + str(self.wiek) + "   " + str(', '.join(self.przedmioty))

def sprawdz_typ(zmienna, typ):
    if not type(zmienna) is typ:
        raise TypeError("Oczekiwano" + typ + " otrzymano " + type(zmienna))

def dodaj_ucznia(uczniowie):
    while 1:
        imie: str = input("podaj imie/stop: ")
        if imie == "stop":
            break
        sprawdz_typ(imie, str)
        wiek = input("podaj wiek: ")
        przedmioty_str = input("podaj przedmioty: ")
        try:
            wiek = int(wiek)
            przedmioty_str = str(przedmioty_str)
        except ValueError:
            print('Wprowadz poprawne typy')
            continue
        else:
            przedmioty = [p.strip() for p in przedmioty_str.split(',')]
            uczen = Uczen(imie,wiek,przedmioty)
            uczniowie[uczen.imie] = uczen

def wyswietl_ucznia(uczniowie):
    print("imie   nazwisko   przedmioty")
    for i in uczniowie.values():
        print(i)

def filtruj_wiek(uczniowie):
    wiek_min = int(input("podaj minimalny wiek: "))
    sprawdz_typ(wiek_min, int)
    for i in uczniowie.values():
        if i.wiek >= wiek_min:
            print(i)
    return wiek_min

def zapisz_csv(uczniowie):
    import csv
    with open('zapis.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        for uczen in uczniowie.values():
            writer.writerow([uczen.imie, uczen.wiek, ','.join(uczen.przedmioty)])

def wczytaj_csv(uczniowie):
    import csv
    with open('zapis.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            przedmioty = [p.strip() for p in row[2].split(',')]
            uczen = Uczen(row[0],int(row[1]),przedmioty)
            uczniowie[row[0]] = uczen

def generator(uczniowie, min_wiek): #Dodatkowy generator tabelki w formie pliku html, ponieważ tabelka miała być ładnie sformatowana
    with open("table.html", "w") as f:
        data = "<!DOCTYPE html><html><head><link rel='stylesheet' href='style.css'><title>Tabelka</title></head><body><h2>Wyświetlanie całej tabelki:</h2><div class='table-wrapper'><table class='fl-table'><tr><th>Imie</th><th>Wiek</th><th>Przedmioty</th></tr>"
        for row in uczniowie.values():
            data += "<tr>"
            data += "<td>"+row.imie+"</td>"
            data += "<td>"+str(row.wiek)+"</td>"
            data += "<td>"+str(', '.join(row.przedmioty))+"</td>"
            data += "</tr>"

        data += f"</table></div><h2>Filtrowanie minimalnego wieku: {min_wiek}</h2><div class='table-wrapper'><table class='fl-table'><tr><th>Imie</th><th>Wiek</th><th>Przedmioty</th></tr>"

        for row in uczniowie.values():
            if row.wiek >= min_wiek:
                data += "<tr>"
                data += "<td>" + row.imie + "</td>"
                data += "<td>" + str(row.wiek) + "</td>"
                data += "<td>" + str(', '.join(row.przedmioty)) + "</td>"
                data += "</tr>"
        f.write(data)
        f.write("</table></body></html>")
        f.close()
        os.startfile("table.html")


def main():
    uczniowie = {}
    wczytac = input("Wczytać plik csv? T?")
    if wczytac == "T":
        wczytaj_csv(uczniowie)

    dodaj_ucznia(uczniowie)
    wyswietl_ucznia(uczniowie)
    wiek_min = filtruj_wiek(uczniowie)

    piekna_tabelka = input("Wyswietlic piekna tabelke? T?")
    if piekna_tabelka == "T":
        generator(uczniowie,wiek_min)
    zapisz_csv(uczniowie)

if __name__ == "__main__":
    main()

