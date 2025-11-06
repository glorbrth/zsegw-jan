import tkinter as tk

def na_najechaniu(e):
    status_panel.config(bg="yellow",text="UZBROJENIE MOŻLIWE")

def na_kliknieciu(e):
    status_panel.config(bg="red",text="SYSTEM UZBROJONY")

def na_opuszczeniu(e):
    status_panel.config(bg="green",text="SYSTEM ROZBROJONY")

root = tk.Tk()
root.title("Panel Alarmowy")
root.geometry("350x150")

status_panel = tk.Label(
    root, 
    text="SYSTEM ROZBROJONY", 
    bg="green", 
    fg="white", 
    font=('Arial', 16, 'bold'),
    width=25,
    height=3
)
status_panel.pack(padx=20, pady=20)

status_panel.bind('<Enter>', na_najechaniu)
status_panel.bind('<Button-1>', na_kliknieciu)
status_panel.bind('<Leave>', na_opuszczeniu)

root.mainloop()