import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
from tkinter import filedialog

# Globalne ustawienia motywu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budżet Domowy")
        self.geometry("1600x800")
        self.minsize(1600, 800)

        self.grid_columnconfigure(0, weight=0, minsize=350)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.money_frame = MoneyFrame(self, on_refresh=self.refresh_charts, width=350)
        self.money_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.scrollable_spending = CategoriesFrame(self, on_change=self.refresh_charts, width=350)
        self.scrollable_spending.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self.pcf = PieChartFrame(self)
        self.pcf.grid(row=0, column=2, rowspan=2, pady=10, padx=10, sticky="nsew")

        self.wpcf = WholePieChartFrame(self)
        self.wpcf.grid(row=0, column=1, rowspan=2, pady=10, padx=10, sticky="nsew")

        # Opóźnienie pierwszego odświeżenia żeby wszystkie elementy się załadowały
        self.after(100, self.refresh_charts)

    def refresh_charts(self, *args):
        if not hasattr(self, 'money_frame') or not hasattr(self, 'scrollable_spending'): #sprawdzic czy sie zrobiło wszystko
            return
        rows = self.scrollable_spending.rows
        sum_wydatkow = self.scrollable_spending.sum
        save = self.money_frame.save
        income = self.money_frame.income

        self.pcf.update_data(rows, sum_wydatkow)
        self.wpcf.update_data(rows, save, income, sum_wydatkow)

    def export_pdf(self):
        if not hasattr(self, 'pcf') or not hasattr(self, 'wpcf'): #sprawdzenie czy sa oba wykresy
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Zapisz wykresy"
        )
        if not file_path:
            return

        fig1 = self.pcf.figure
        fig2 = self.wpcf.figure

        with PdfPages(file_path) as pdf:
            pdf.savefig(fig1, bbox_inches='tight')
            pdf.savefig(fig2, bbox_inches='tight')


class MoneyFrame(ctk.CTkFrame):
    def refresh(self, event=None):
        try: #przychod
            self.income = int(self.input_income.get())
            if self.income < 0:
                self.income = 0
        except ValueError:
            self.income = 0

        try: #oszczednosci
            self.save = int(self.input_save.get())
            if self.save < 0:
                self.save = 0
        except ValueError:
            self.save = 0

        if self.on_refresh:
            self.on_refresh()

    def __init__(self, master, on_refresh=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_refresh = on_refresh
        self.income = 0
        self.save = 0

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        self.lbl_income = ctk.CTkLabel(self, text="Podaj przychód", font=("Helvetica", 18))
        self.lbl_income.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.input_income = ctk.CTkEntry(self)
        self.input_income.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
        self.input_income.bind("<KeyRelease>", self.refresh)

        self.lbl_save = ctk.CTkLabel(self, text="Podaj oszczędności", font=("Helvetica", 18))
        self.lbl_save.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        self.input_save = ctk.CTkEntry(self)
        self.input_save.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        self.input_save.bind("<KeyRelease>", self.refresh)

        self.btn_export = ctk.CTkButton(
            self, text="Eksportuj do PDF", command=self.export_callback, fg_color="#2c7a4d", hover_color="#1e5a38"
        )
        self.btn_export.grid(row=2, column=0, columnspan=2, pady=15, padx=10, sticky="ew")

    def export_callback(self):
        if self.master and hasattr(self.master, 'export_pdf'):
            self.master.export_pdf()


class CategoriesFrame(ctk.CTkScrollableFrame):
    def add_row(self):
        self.values += 1
        lbl = ctk.CTkLabel(self, text=self.entry.get(), font=("Helvetica", 18))
        lbl.grid(row=self.values, column=0, pady=5, padx=10, sticky="w")

        entry = ctk.CTkEntry(self)
        entry.grid(row=self.values, column=1, pady=5, padx=10, sticky="ew")
        entry.bind("<KeyRelease>", self.on_entry_change)
        self.rows.append((lbl, entry))

        self.calculate_sum()

    def on_entry_change(self, event=None):
        self.calculate_sum()
        if self.on_change:
            self.on_change()

    def calculate_sum(self, event=None):
        self.sum = 0
        if not self.rows:
            return
        for lbl, ent in self.rows:
            try:
                val = int(ent.get())
                if val > 0:
                    self.sum += val
            except ValueError:
                continue

    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, **kwargs)
        self.values = 0
        self.sum = 0
        self.rows = []
        self.on_change = on_change

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.entry = ctk.CTkEntry(self, placeholder_text="Nazwa kategorii")
        self.entry.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        self.btn_add = ctk.CTkButton(self, text="Dodaj kategorię", command=self.add_row)
        self.btn_add.grid(row=0, column=1, pady=10, padx=10, sticky="ew")


class PieChartFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#242424")
        self.figure.set_facecolor("#242424")

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.bind("<Configure>", self.on_resize)
        self.update_data([], 0)

    def update_data(self, rows, total_sum):
        self.ax.clear()
        self.ax.set_facecolor("#242424")

        if rows and total_sum > 0:
            values = []
            labels = []
            for lbl, ent in rows:
                try:
                    val = int(ent.get())
                    if val > 0:
                        values.append(val)
                        labels.append(lbl.cget("text"))
                except ValueError:
                    continue
        else:
            values = [100]
            labels = ["Brak danych"]

        if values and labels != ["Brak danych"]:
            total = sum(values)
            self.ax.pie(
                values,
                labels=labels,
                autopct=lambda pct: f'{pct/100 * total:.0f} zł',
                textprops={'color': 'white'},
                startangle=90,
                labeldistance=1.1
            )
        else:
            self.ax.pie([100], labels=["Brak danych"], textprops={'color': 'white'})

        self.ax.axis('equal')
        self.canvas.draw_idle()

    def on_resize(self, event):
        if event.widget == self:
            new_width = max(1, event.width / self.figure.dpi)
            new_height = max(1, event.height / self.figure.dpi)
            self.figure.set_size_inches(new_width, new_height)
            self.canvas.draw_idle()


class WholePieChartFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#242424")
        self.figure.set_facecolor("#242424")

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.bind("<Configure>", self.on_resize)
        self.update_data([], 0, 0, 0)

    def update_data(self, rows, save_amount, income, total_expenses_sum):
        self.ax.clear()
        self.ax.set_facecolor("#242424")

        values = []
        labels = []

        if rows and income > 0:
            total = 0
            for lbl, ent in rows:
                try:
                    val = int(ent.get())
                    if val > 0:
                        values.append(val)
                        labels.append(lbl.cget("text"))
                        total += val
                except ValueError:
                    continue

            if save_amount > 0:
                values.append(save_amount)
                labels.append("Oszczędności")
                total += save_amount

            rest = income - total
            if rest > 0:
                values.append(rest)
                labels.append("Pozostało")
        else:
            values = [100]
            labels = ["Brak danych"]

        if labels != ["Brak danych"]:
            total = sum(values)
            self.ax.pie(
                values,
                labels=labels,
                autopct=lambda pct: f'{pct/100 * total:.0f} zł',
                textprops={'color': 'white'},
                startangle=90,
                labeldistance=1.1
            )
        else:
            self.ax.pie([100], labels=["Brak danych"], textprops={'color': 'white'})

        self.ax.axis('equal')
        self.canvas.draw_idle()

    def on_resize(self, event):
        if event.widget == self:
            new_width = max(1, event.width / self.figure.dpi)
            new_height = max(1, event.height / self.figure.dpi)
            self.figure.set_size_inches(new_width, new_height)
            self.canvas.draw_idle()


if __name__ == "__main__":
    app = App()
    app.mainloop()