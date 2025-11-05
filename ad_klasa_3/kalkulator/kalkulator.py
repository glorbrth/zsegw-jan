import tkinter
from tkinter import *

data: str = "" #GLOBAL CURRENT DATA ex. (144+123)

def add_data(operand):
    global data
    data += str(operand)
    result.set(data)

def calculate():
    try:
        global data
        if data == "":
            result.set("")
        else:
            data_sum = str(eval(data)) #no need for float, as python is so intelligent it knows and adds float type when there is decimal point
            result.set(data_sum)
            data = data_sum
    except:
        result.set("ERROR")
        data = ""

def clear():
    global data
    data = ""
    result.set("")

def print_result(*args):
    res = result.get()
    print(res)

if __name__ == "__main__":
    window = Tk()
    window.title("Kalkulator")
    window.geometry("300x500")
    window.minsize(150, 200)  #SMALLER BREAKS

    #ADDING WEIGHT FOR SCALING TO WORK
    for i in range(6):
        window.grid_rowconfigure(i, weight=1)
    for i in range(4):
        window.grid_columnconfigure(i, weight=1)

    result = StringVar() #currently displayed data

    #TEXT FIELD
    field = tkinter.Entry(window,state='readonly',textvariable=result)
    field.grid(columnspan=4,sticky="nsew",padx=10,pady=10,ipady=10)

    #@DEBUG result.trace_add("write", print_result)

    #SCALABLE BUTTONS
    btn_config = {
        'sticky': 'nsew',
    }

    #BUTTONS:
    button0 = Button(window, text="0", command=lambda: add_data(0))
    button0.grid(row=2, column=0, **btn_config)

    button1 = Button(window, text="1", command=lambda: add_data(1))
    button1.grid(row=2, column=1, **btn_config)

    button2 = Button(window, text="2", command=lambda: add_data(2))
    button2.grid(row=2, column=2, **btn_config)

    button3 = Button(window, text="3", command=lambda: add_data(3))
    button3.grid(row=3, column=0, **btn_config)

    button4 = Button(window, text="4", command=lambda: add_data(4))
    button4.grid(row=3, column=1, **btn_config)

    button5 = Button(window, text="5", command=lambda: add_data(5))
    button5.grid(row=3, column=2, **btn_config)

    button6 = Button(window, text="6", command=lambda: add_data(6))
    button6.grid(row=4, column=0, **btn_config)

    button7 = Button(window, text="7", command=lambda: add_data(7))
    button7.grid(row=4, column=1, **btn_config)

    button8 = Button(window, text="8", command=lambda: add_data(8))
    button8.grid(row=4, column=2, **btn_config)

    button9 = Button(window, text="9", command=lambda: add_data(9))
    button9.grid(row=5, column=0, **btn_config)

    #CLEAR:
    button_clear = Button(window, text="C", command=lambda: clear())
    button_clear.grid(row=5, column=1, **btn_config)

    #SUBMIT:
    button_submit = Button(window, text="=", command=lambda: calculate())
    button_submit.grid(row=5, column=2, **btn_config)

    #OPERATIONS:
    button_add = Button(window, text="+", command=lambda: add_data("+"))
    button_add.grid(row=2, column=3, **btn_config)

    button_subtract = Button(window, text="-", command=lambda: add_data("-"))
    button_subtract.grid(row=3, column=3, **btn_config)

    button_multiply = Button(window, text="*", command=lambda: add_data("*"))
    button_multiply.grid(row=4, column=3, **btn_config)

    button_divide = Button(window, text="/", command=lambda: add_data("/"))
    button_divide.grid(row=5, column=3, **btn_config)

    window.mainloop()