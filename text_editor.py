from tkinter import *
import tkinter.filedialog as tk
import tkinter.messagebox as tk2

root = Tk()

"""
def word_count(text, word_count_label):
    all_text = text.get("1.0", "end")
    #word_count_label.config(textvariable = "Woord Count: " + str(len(all_text.split())))
    tk2.showinfo("Word Count: ", len(all_text.split()))
"""

def word_count(text, word_count_label):
    all_text = text.get("1.0", "end")
    word_count = len(all_text.split())
    word_count_label.destroy()
    word_count_label = Label(info_frame, text = "Word Count: " + str(word_count))
    word_count_label.pack()
    return word_count_label
    
root.option_add("*tearOff", FALSE) # prevents menu options from being torn off

label = Label(root, text = "Copyright Arnab Sen 2017")
label.pack()

text_frame = Frame(root)
text_frame.pack(expand = 1, fill = BOTH)

text = Text(text_frame)
text.pack(expand = 1, fill = BOTH)

info_frame = Frame(root)
info_frame.pack(side = BOTTOM)

current_word_count = 0
word_count_label = Label(info_frame, text = "Word Count: 0", textvariable = current_word_count\
                         , justify = "right")
word_count_label.pack()
#word_count_label.pack_forget()


# Menubar          
menu_bar = Menu(root)
menu_bar.add_command(label = "Word Count", command = lambda: \
                     word_count(text, word_count_label)) # calls word_count()
root.config(menu = menu_bar)

# pulldown menus

root.mainloop()
