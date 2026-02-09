import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.entry = tk.Entry(self)
        self.entry.pack()
        self.label = tk.Label(self, text="Czekam...")
        self.label.pack()
        self.btn = tk.Button(self, text="Powitaj", command=self.say_hello)
        self.btn.pack()
        self.clear = tk.Button(self, text="Wyczysc", command=self.clear_data)
        self.clear.pack()

    def say_hello(self):
        name = self.entry.get()
        self.label.config(text=f"Witaj, {name}!")
    
    def clear_data(self):
        self.entry.delete(0,'end')
        self.label.config(text="")

import unittest

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.withdraw() # Ukrywamy okno podczas testów

    def tearDown(self):
        self.app.destroy()

    def test_greeting(self):
        # 1. Symulacja wpisania tekstu
        self.app.entry.insert(0, "Jan")
        
        # 2. Symulacja kliknięcia (wywołanie komendy przycisku)
        self.app.btn.invoke()
        
        # 3. Sprawdzenie wyniku
        result = self.app.label.cget("text")
        self.assertEqual(result, "Witaj, Jan!")
    
    def test_clear(self): #Ćwiczenie 1
        self.app.entry.insert(0,"Filip")
        self.app.clear.invoke()

        self.assertEqual(self.app.entry.get(), "")
        self.assertEqual(self.app.label.cget("text"), "")
    
    def test_visible_widget(self):
        self.app.update()
        assertTrue(self.app.btn.winfo_ismapped())

if __name__ == "__main__":
    #app = App()
    #app.mainloop()
    unittest.main()
    