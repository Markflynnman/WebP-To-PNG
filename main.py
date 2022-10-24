import os
import sys
from send2trash import send2trash
from tkinter import *
from tkinter import ttk, filedialog
import customtkinter
from PIL import Image

BACKGROUND = "#fafafa"
BLUE = "#1F6AA5"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def delete_toggle():
    if delete.get() == 0 or delete.get() == 2:
        delete.set(1)
        delete_check.configure(fg_color=BLUE)
        safemode_check.configure(fg_color=None)
    else:
        delete.set(0)
        delete_check.configure(fg_color=None)


def safemode_toggle():
    if delete.get() == 0 or delete.get() == 1:
        delete.set(2)
        safemode_check.configure(fg_color=BLUE)
        delete_check.configure(fg_color=None)
    else:
        delete.set(0)
        safemode_check.configure(fg_color=None)


def select_file():
    folder_dir = filedialog.askdirectory(title="Select root folder", initialdir=os.getcwd())
    DIR.set(folder_dir)


def convert_files():
    dir_found = False
    feedback_text.set("")
    screen.update()
    for (root, dirs, files) in os.walk(DIR.get(), topdown=True):
        dir_found = True
        for file in files:
            if ".webp" in file:
                WebP = root + "/" + file
                FileName = file.replace(".webp", "")

                img_webp = WebP
                img_png = root + "\\" + FileName + ".png"

                im = Image.open(img_webp)
                im.save(img_png, format="png", lossless=True)

                feedback.configure(fg="green")
                feedback_text.set(img_webp.replace("/", "\\"))
                feedback.configure(anchor=W)
                screen.update()

                if delete.get() == 1:
                    os.remove(img_webp)
                elif delete.get() == 2:
                    send2trash(img_webp.replace("/", "\\"))

    if not dir_found:
        feedback_text.set("Directory not found")
        feedback.configure(fg="red")
        feedback.configure(anchor=CENTER)
    else:
        feedback_text.set("Converted!")
        feedback.configure(fg="green")
        feedback.configure(anchor=CENTER)


customtkinter.set_appearance_mode("System")
screen = customtkinter.CTk()
screen.geometry("500x300")
screen.minsize(500, 300)
screen.title("WebP to PNG")

screen.grid_rowconfigure(4, weight=1)
screen.columnconfigure((0, 1), weight=0)
screen.columnconfigure((2, 3), weight=1)

screen.iconbitmap(resource_path("icon.ico"))


delete = IntVar()
feedback_text = StringVar()
DIR = StringVar(value=os.getcwd())
s = ttk.Style()
s.configure("Background.TCheckbutton", background=BACKGROUND)
s.configure("Background.TButton", background=BACKGROUND, forground=BACKGROUND)

dir_label = customtkinter.CTkLabel(screen, text="Folder", text_font=("default_theme", 20))
dir_label.grid(row=0, column=0, padx=0, pady=(15, 5), sticky="w")
dir_entry = customtkinter.CTkEntry(screen, textvariable=DIR, width=400, background=BACKGROUND)
dir_entry.grid(row=1, column=0, padx=(30, 5), pady=5, sticky="nw", columnspan=3)

browse = customtkinter.CTkButton(screen, text="Browse", command=select_file, width=150)
browse.grid(row=1, column=3, padx=(5, 30), pady=5, sticky="nw")

delete_label = customtkinter.CTkLabel(screen, text="Delete", text_font=("default_theme", 20))
delete_label.grid(row=2, column=0, padx=0, pady=(20, 5), sticky="w")
delete_check = customtkinter.CTkButton(screen, text="Delete", border_width=2, border_color=BLUE, fg_color=None,
                                       command=delete_toggle, hover=False, width=100)
delete_check.grid(row=3, column=0, padx=(30, 5), pady=5, sticky="w")

safemode_check = customtkinter.CTkButton(screen, text="Delete (safemode)", border_width=2, border_color=BLUE,
                                         fg_color=None, command=safemode_toggle, hover=False, width=50)
safemode_check.grid(row=3, column=1, padx=5, pady=5, sticky="e")

feedback = customtkinter.CTkLabel(screen, textvariable=feedback_text, background=BACKGROUND)
feedback.grid(row=4, column=0, padx=10, pady=20, sticky="n", columnspan=4)

convert = customtkinter.CTkButton(screen, text="Convert", command=convert_files, width=100)
convert.grid(row=5, column=0, padx=(30, 30), pady=(0, 15), sticky="nwe", columnspan=4)

screen.mainloop()

