from tkinter import *

def add():
    result.config(text=float(num1.get()) + float(num2.get()))

def subtract():
    result.config(text=float(num1.get()) - float(num2.get()))

def multiply():
    result.config(text=float(num1.get()) * float(num2.get()))

def divide():
    result.config(text=float(num1.get()) / float(num2.get()))

root = Tk()
root.title("Calculator")

Label(root, text="First Number").pack()
num1 = Entry(root)
num1.pack()

Label(root, text="Second Number").pack()
num2 = Entry(root)
num2.pack()

result = Label(root, text="Result")
result.pack()

menu = Menu(root)
root.config(menu=menu)

calc = Menu(menu, tearoff=0)
menu.add_cascade(label="Operations", menu=calc)

calc.add_command(label="Addition", command=add)
calc.add_command(label="Subtraction", command=subtract)
calc.add_command(label="Multiplication", command=multiply)
calc.add_command(label="Division", command=divide)

root.mainloop()