import tkinter as tk
# from tkinter.ttk import *
from PIL import Image, ImageTk
from itertools import count, cycle

from threading import Thread


class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


root = tk.Tk()

main_frame = tk.Frame(master=root, bg='black')

# style = Style()

# style.configure("Horizontal.TScrollbar", gripcount=0,
#                 background="Green", darkcolor="DarkGreen", lightcolor="LightGreen",
#                 troughcolor="gray", bordercolor="blue", arrowcolor="white")

lbl = ImageLabel(root)

lbl.pack()
lbl.load('1_wX8RI80-FKhbP0ODlQrEQw.gif')

chat_listbox = tk.Listbox(master=main_frame, height=80, width=63, selectmode=tk.EXTENDED, bg='black', fg='white')
chat_listbox.xview()
xscroll_bar = tk.Scrollbar(master=main_frame, orient='horizontal', width=1, command=chat_listbox.xview)
yscroll_bar = tk.Scrollbar(master=main_frame, orient='vertical', width=1, command=chat_listbox.yview)
speak_button = tk.Button(master=root, text='Speak', font=("Ariel", 12), command=lambda: None,fg='white', bg='black', bd=4, height=2, width= 50)

chat_listbox['xscrollcommand'] = xscroll_bar.set
chat_listbox['yscrollcommand'] = yscroll_bar.set

def set_speak_command(command):
    speak_button.configure(command=command)


def speak(text):
    chat_listbox.insert('end', f'Assistant: {text}')


xscroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
yscroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

chat_listbox.pack(fill=tk.Y, side=tk.RIGHT)


speak_button.pack(anchor=tk.SW, side=tk.BOTTOM)


xscroll_bar.configure(command=chat_listbox.xview)
yscroll_bar.configure(command=chat_listbox.yview)

main_frame.pack(fill=tk.BOTH)
root.geometry('400x600')
root.minsize(400, 600)
root.wm_title('Elvis')
root.resizable(False, True)
mainloop = root.mainloop


# mainloop()