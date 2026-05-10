import tkinter as tk

display = ""

def press(val):
    global display
    display += str(val)
    entry.delete(0, tk.END)
    entry.insert(0, display)

def equal():
    global display
    try:
        result = str(eval(display))
        entry.delete(0, tk.END)
        entry.insert(0, result)
        display = result
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        display = ""

def clear():
    global display
    display = ""
    entry.delete(0, tk.END)

root = tk.Tk()

root.title("Calc")

entry = tk.Entry(root, width=16, font=("Arial", 18), justify="right")
entry.grid(row=0, column=0, columnspan=4)

buttons = [
    "7","8","9","/",
    "4","5","6","*",
    "1","2","3","-",
    "0",".","=","+",
]

r, c = 1, 0
for b in buttons:
    cmd = equal if b == "=" else lambda x=b: press(x)
    tk.Button(root, text=b, width=4, height=2, command=cmd).grid(row=r, column=c)
    c += 1
    if c == 4:
        c = 0
        r += 1

tk.Button(root, text="C", width=16, height=2, command=clear).grid(row=r, column=0, columnspan=4)
root.geometry("240x290")
root.resizable(False, False)
root.mainloop()