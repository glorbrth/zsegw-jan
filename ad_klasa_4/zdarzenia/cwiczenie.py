import tkinter as tk

def aktualizuj_wspolrzedne(event):
    # Uzupełnij kod tutaj
    pass # Usuń 'pass' i dodaj logikę

root = tk.Tk()
root.title("Śledzenie Myszki")
root.geometry("300x200")

coords_label = tk.Label(root, text="Pozycja: (X: ?, Y: ?)", font=('Arial', 14))
coords_label.pack(pady=50)

def move_mouse(e):
    coords_label.config(text=f"X: {e.x} Y: {e.y}")

root.bind('<Motion>',move_mouse)

root.mainloop()