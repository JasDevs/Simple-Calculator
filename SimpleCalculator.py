import tkinter as tk
import re
import time as t
from tkinter import *
from ctypes import windll

regularFontStyle = ("Roboto Regular", 30, "bold")
mediumFontStyle = ("Fira Code", 35)
largeFontStyle = ("Fira Code", 50, "bold")

digitsFontStyle = ("Fira Code", 25, "bold")
specialFontStyle = ("Fira Code", 25, "bold")

backgroundColor = "#383e4a"
buttonColor = "#494f5c"
buttonColor2 = "#565c6b"
frameColor = "#3c424d"

fadedWhiteColor = "#bababa"
whiteColor = "#f5f5f5"
darkerBlueColor = "#4f9cdb"
darkBlueColor = "#4b90c9"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("300x500")
        self.window.minsize(300,500)
        self.window.maxsize(355, 667)

        self.window.title("Simple Calculator")
        self.window.iconbitmap('C:\\Users\\Owner\\Desktop\\CodeFolders\\PythonApps\\SimpleCalculator\\favicon.ico')

        self.totalExpression = ""
        self.currentExpression = ""

        self.displayFrame = self.createDisplayFrame()
        self.totalLabel, self.label = self.createDisplayLabels()
        self.buttonsFrame = self.createButtonsFrame()

        self.digits = {
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2),
            ".": (4, 1),
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "\u2212", "+": "\u002B"}

        for x in range(1, 5):
            self.buttonsFrame.rowconfigure(x, weight=1)
            self.buttonsFrame.columnconfigure(x, weight=1)
        self.createDigitButtons()
        self.createOperatorButtons()
        self.createSpecialButtons()
        self.bindKeys()
            
    def bindKeys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())

        self.window.bind("c", lambda event: self.clear())
        self.window.bind("<Delete>", lambda event: self.clear())
        self.window.bind("<BackSpace>", lambda event: self.clear())

        self.window.bind("r", lambda event: self.sqrt())
        self.window.bind("s", lambda event: self.square())

        for key in self.digits:
            self.window.bind(
                str(key), lambda event, digit=key: self.addToExpression(digit)
            )
        for key in self.operations:
            self.window.bind(
                str(key), lambda event, operator=key: self.appendOperator(operator)
            )

    def createSpecialButtons(self):
        self.createClearButton()
        self.createEqualsButton()
        self.createSquareButton()
        self.createSquareRootButton()

    def createDisplayLabels(self):
        totalLabel = tk.Label(
            self.displayFrame,
            text=self.totalExpression,
            anchor=tk.E,
            bg=frameColor,
            fg=fadedWhiteColor,
            padx=24,
            font=regularFontStyle,
        )
        label = tk.Label(
            self.displayFrame,
            text=self.currentExpression,
            anchor=tk.E,
            bg=frameColor,
            fg=whiteColor,
            padx=24,
            font=largeFontStyle,
        )
        totalLabel.pack(expand=True, fill="both")
        label.pack(expand=True, fill="both")
        return totalLabel, label

    def createDisplayFrame(self):
        frame = tk.Frame(self.window, height=221, bg=backgroundColor)
        frame.pack(expand=True, fill="both")
        return frame

    def addToExpression(self, value):
        self.currentExpression += str(value)
        self.updateLabel()

    def createDigitButtons(self):
        for digit, gridValue in self.digits.items():
            button = tk.Button(
                self.buttonsFrame,
                text=str(digit),
                bg=buttonColor,
                fg=whiteColor,
                font=digitsFontStyle,
                borderwidth=0,
                command=lambda x=digit: self.addToExpression(x),
            )
            button.grid(row=gridValue[0], column=gridValue[1], sticky=tk.NSEW)

    def appendOperator(self, operator):
        self.currentExpression += operator
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.updateTotalLabel()
        self.updateLabel()

    def createOperatorButtons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(
                self.buttonsFrame,
                text=symbol,
                bg=darkBlueColor,
                fg=whiteColor,
                font=specialFontStyle,
                borderwidth=0,
                command=lambda x=operator: self.appendOperator(x),
            )
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.currentExpression = ""
        self.updateLabel()
        self.totalExpression = ""
        self.updateTotalLabel()

    def createClearButton(self):
        button = tk.Button(
            self.buttonsFrame,
            text="C",
            bg=buttonColor,
            fg=whiteColor,
            font=specialFontStyle,
            borderwidth=0,
            command=self.clear,
        )
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def sqrt(self):
        self.currentExpression = str(eval(f"{self.currentExpression}**0.5"))
        self.updateLabel()
        self.updateTotalLabel()

    def createSquareRootButton(self):
        button = tk.Button(
            self.buttonsFrame,
            text="√",
            bg=buttonColor2,
            fg=whiteColor,
            font=specialFontStyle,
            borderwidth=0,
            command=self.square,
        )
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def square(self):
        self.currentExpression = str(eval(f"{self.currentExpression}**2"))
        self.updateLabel()
        self.updateTotalLabel()

    def createSquareButton(self):
        button = tk.Button(
            self.buttonsFrame,
            text="x\u00b2",
            bg=buttonColor2,
            fg=whiteColor,
            font=specialFontStyle,
            borderwidth=0,
            command=self.square,
        )
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.totalExpression += self.currentExpression
        self.updateTotalLabel()
        try:
            self.currentExpression = str(eval(self.totalExpression))
            self.totalExpression = ""
        except Exception as a:
            self.clear()
        finally:
            self.updateLabel()

    def createEqualsButton(self):
        button = tk.Button(
            self.buttonsFrame,
            text="=",
            bg=darkerBlueColor,
            fg=whiteColor,
            font=specialFontStyle,
            borderwidth=0,
            command=self.evaluate,
        )
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def createButtonsFrame(self):
        frame = tk.Frame(self.window, bg=backgroundColor)
        frame.pack(expand=True, fill="both")
        return frame

    def updateTotalLabel(self):
        self.totalLabel.config(
            text=re.sub("(?<=[^0-9 ])[^0-9 ]", "", self.totalExpression)[:10]
        )

    def updateLabel(self):
        self.label.config(
            text=re.sub("(?<=[^0-9 ])[^0-9 ]", "", self.currentExpression)[:7]
        )


calc = Calculator()
calc.window.mainloop()
