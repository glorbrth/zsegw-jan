import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.entry1 = tk.Entry(self)
        self.entry1.pack()
        self.entry2 = tk.Entry(self)
        self.entry2.pack()
        self.btn = tk.Button(self, text="Oblicz", command=self.oblicz)
        self.btn.pack()
        self.label = tk.Label(self, text="")
        self.label.pack()

    def oblicz(self):
        num1 = self.entry1.get()
        num2 = self.entry2.get()
        try:
            num1 = int(num1)
            num2 = int(num2)
        except ValueError:
            self.label.config(text="Błąd danych")
            return
        res = num1+num2
        self.label.config(text=str(res))

import unittest

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.withdraw() # Ukrywamy okno podczas testów

    def tearDown(self):
        self.app.destroy()

    def test_ints(self):
        self.app.entry1.insert(0, "5")
        self.app.entry2.insert(0, "10")
        self.app.btn.invoke()
        result = self.app.label.cget("text")
        self.assertEqual(result, "15")
    
    def test_str_and_int(self): #Ćwiczenie 1
        self.app.entry1.insert(0, "abc")
        self.app.entry2.insert(0, "1")
        self.app.btn.invoke()
        result = self.app.label.cget("text")
        self.assertEqual(result, "Błąd danych")
    
    def test_empty(self): #Ćwiczenie 1
        self.app.entry1.insert(0, "")
        self.app.entry2.insert(0, "")
        self.app.btn.invoke()
        result = self.app.label.cget("text")
        self.assertEqual(result, "Błąd danych")
    
if __name__ == "__main__":
    #app = App()
    #app.mainloop()
    unittest.main()