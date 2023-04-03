import os
import sys
import json
import tkinter
from tkinter import messagebox
from difflib import SequenceMatcher
import customtkinter
from customtkinter import CTk as ctk


def restart():

    """ RESTARTS THE PROGRAM """

    python = sys.executable
    os.execl(python, python, *sys.argv)

def showMeaning():

    """ DISPLAYS THE MEANING TEXT ON THE GUI """

    if myVar.get() == "":
        messagebox.showwarning("Error", "Enter a word!")

    else:
        getMeaning(myVar.get())
        with open("textStore.txt", "r") as np:
            meaningTextText = tkinter.Text(mainframe, height=20, width=70, wrap="word", font=("arial", 15),
                                           background="grey", borderwidth=15)
            meaningTextText.insert(tkinter.END, np.read())
            meaningTextText.pack()

            okayButton = customtkinter.CTkButton(mainframe, command=restart, text="Okay", width=70,
                                                 bg_color="grey", border_width=1, border_color="white", fg_color="grey")
            okayButton.place(x=582, y=334)

def getMeaning(word):

    """  EXTRACTS THE MEANING OF THE INPUT WORD FROM THE JSON OBJECT """
    word = word.lower()
    meanings = []
    numberOfDefinitions = 0
    definitionNumber = 0

    with open("textStore.txt", "w") as sp:
        sp.write("")
        sp.close()

    with open("data.json") as fpt:
        dataObject = json.load(fpt)

    if word in dataObject.keys():
        with open("textStore.txt", "w") as abf:
            abf.write(f"{word.capitalize()} :\n \n")
            abf.close()

        for defs in dataObject[word]:
            numberOfDefinitions = numberOfDefinitions + 1
            definitionNumber = definitionNumber + 1
            meanings.append(str(definitionNumber) + ": " + defs)

            with open("textStore.txt", "a") as bf:
                bf.write(str(definitionNumber) + " .   " + defs + "\n \n")
                bf.close()

    else:
        nothing = ""
        suggestionsList = []
        orWord = "or"
        for key in dataObject.keys():
            matchValue = SequenceMatcher(a=word, b=key)
            if matchValue.ratio() >= 0.8:
                suggestionsList.append(key)

        if len(suggestionsList) > 0:
            responseText = str(
                f"   did you mean {suggestionsList[0].capitalize() if len(suggestionsList) >= 1 else nothing} {orWord if len(suggestionsList) >= 2 else nothing} {suggestionsList[1].capitalize() if len(suggestionsList) >= 2 else nothing} {orWord if len(suggestionsList) >= 3 else nothing} {suggestionsList[2].capitalize() if len(suggestionsList) >= 3 else nothing} {orWord if len(suggestionsList) >= 4 else nothing} {suggestionsList[3].capitalize() if len(suggestionsList) >= 4 else nothing}?"
            )
            with open("textStore.txt", "w") as nfp:
                if len(suggestionsList) > 0:
                    nfp.write(f"\n   \"{word.capitalize()}\" not found! \n \n \n")
                    nfp.close()
            with open("textStore.txt", "a") as nfp:
                nfp.write(responseText)
                nfp.close()
            return responseText

        else:
            responseText = "\n Not found !"
            with open("textStore.txt", "w") as kfp:
                kfp.write("")
                kfp.close()
            with open("textStore.txt", "a") as mfp:
                mfp.write(responseText)
                mfp.close()
            return responseText


# THE GUI
root = ctk()
myVar = customtkinter.StringVar()
myVar.set(myVar.get())
root.title("SAADAT DICTIONARY v1.0")
w = 700
h = 700

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

padding_x = (screen_w / 2) - (w / 2)
padding_y = (screen_h / 2) - (h / 2)

root.geometry("%dx%d+%d+%d" % (w, h, padding_x, padding_y))
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

mainframe = customtkinter.CTkFrame(root, width=w, height=h, fg_color="white")
mainframe.grid(row=0, column=0)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

enterText = customtkinter.CTkLabel(mainframe, text_color="black", text="Enter a word:", font=("arial", 30))
enterText.place(x=250, y=150)

entry = customtkinter.CTkEntry(mainframe, height=40, textvariable=myVar, fg_color="white", text_color="black")
entry.place(x=267, y=200)

button = customtkinter.CTkButton(mainframe, command=showMeaning, text="Check")
button.place(x=267, y=250)

root.mainloop()
