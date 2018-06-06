from tkinter import *

def changeColor() :
    if btnCalculate['fg'] == 'blue' :
        btnCalculate['fg'] = 'red'
    else :
        btnCalculate['fg'] = 'blue'

window = Tk()
window.title('Button')
btnCalculate = Button(window, text = 'Calculate', fg = 'blue', bg = 'light gray', command = changeColor)
btnCalculate.grid(padx=75, pady=15)
window.mainloop()
