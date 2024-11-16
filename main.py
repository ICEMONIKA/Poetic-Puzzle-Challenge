import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class GuessIdiom:
    def __init__(self, master):
        self.master = master
        self.master.title('古诗词挑战')
        self.master.geometry('400x300')

        self.mode_options = ["四字词语", "六字成语"]
        self.mode = tk.StringVar(value=self.mode_options[0])

        self.mode_menu = ttk.OptionMenu(master, self.mode, *self.mode_options, command=self.new_idiom)
        self.mode_menu.pack(pady=10)

        self.label_text = tk.StringVar()
        self.label = ttk.Label(master, textvariable=self.label_text)
        self.label.pack(pady=10)

        self.entry = ttk.Entry(master)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda _: self.check_guess())

        self.button = ttk.Button(master, text='提交', command=self.on_button_click)
        self.button.pack(pady=10)

        self.new_idiom()

    def new_idiom(self, *_):
        mode = self.mode.get()
        filename = f'{["1", "2"][self.mode_options.index(mode)]}.txt'

        with open(filename, 'r', encoding='utf-8') as f:
            idioms = [line.strip() for line in f]

        self.idiom = random.choice(idioms)
        self.missing_char_index = random.choice([i for i, char in enumerate(self.idiom) if char.isalnum()])

        self.label_text.set(f'猜一个成语: {self.idiom[:self.missing_char_index]}_{self.idiom[self.missing_char_index + 1:]}')
        self.entry.delete(0, tk.END)

    def on_button_click(self):
        self.check_guess()

    def check_guess(self):
        guess = self.entry.get()

        if guess == self.idiom[self.missing_char_index]:
            messagebox.showinfo("结果", f'恭喜你，你猜对了！。')
        else:
            messagebox.showinfo("结果", f'很遗憾，你猜错了。正确答案是："{self.idiom[self.missing_char_index]}"')

        self.new_idiom()

root = tk.Tk()
my_gui = GuessIdiom(root)
root.mainloop()
