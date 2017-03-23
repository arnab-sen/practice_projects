from tkinter import *
import tkinter.filedialog as tk
import tkinter.messagebox as tk2

class Application(Frame): # inheriting from class Frame

    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.text1 = Text(height = 20)
        # no need for Text(root, height = 20) as this is within Application
        # (which inherits from Frame)
        self.text1.pack(expand = YES, fill = BOTH) # expand to fit window

        self.option_add("*tearOff", FALSE) # prevents menu options from being torn off
        menubar = Menu(self)
        filemenu = Menu(menubar)
        editmenu = Menu(menubar)
        toolsmenu = Menu(menubar)

        filemenu.add_command(label = "New", command = self.new_doc)
        filemenu.add_command(label = "Open", command = self.open_doc)
        filemenu.add_command(label = "Save", command = self.save_doc)

        editmenu.add_command(label = "Copy", command = self.copy)
        editmenu.add_command(label = "Paste", command = self.paste)
        editmenu.add_command(label = "Clear", command = self.clear)

        toolsmenu.add_command(label = "Word Count", command = self.word_count)

        menubar.add_cascade(label = "File", menu = filemenu)
        menubar.add_cascade(label = "Edit", menu = editmenu)
        menubar.add_cascade(label = "Tools", menu = toolsmenu)

        root.config(menu = menubar)

    def new_doc(self):
        if (tk2.askyesnocancel("Warning", "Unsaved work will be lost. Continue?")): # yes == True, no == False
            self.text1.delete("1.0", END)

    def save_doc(self):
        save_file = tk.asksaveasfile(mode = "w", defaultextension = ".txt")
        text_to_save = str(self.text1.get("1.0", END)) # what type does get() retrieve by default? Not string?
        save_file.write(text_to_save)
        save_file.close()

    def open_doc(self):
        open_file = tk.askopenfile(mode = "r")
        text = open_file.read()
        self.text1.insert(END, text)
        open_file.close()

    def copy(self):
        copy_text = str(self.text1.get(SEL_FIRST, SEL_LAST))
        self.clipboard_clear()
        self.clipboard_append(copy_text)

    def paste(self):
        paste_text = self.selection_get(selection = "CLIPBOARD")
        self.text1.insert("1.0", paste_text)

    def clear(self):
        self.text1.delete("1.0", END)

    def word_count(self):
        all_text = self.text1.get("1.0", END)
        word_count = len(all_text.split())
        tk2.showinfo("", "Word Count: " + str(word_count))

root = Tk()
root.title("My Text Editor")
root.geometry("800x600")
program = Application(root)
program.mainloop()
