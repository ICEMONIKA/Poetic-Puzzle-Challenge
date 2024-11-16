import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

class GuessIdiom:
    def __init__(self, master):
        self.master = master
        self.master.title('古诗词挑战')
        self.master.geometry('400x400')
        self.master.configure(bg='lightblue')  # 背景颜色

        # 难度选择
        self.difficulty_options = ["无限制", "易", "中", "难"]
        self.difficulty = tk.StringVar(value=self.difficulty_options[0])
        self.difficulty_menu = ttk.OptionMenu(master, self.difficulty, *self.difficulty_options, command=self.new_idiom)
        self.difficulty_menu.pack(pady=10)

        # 模式选择
        self.mode_options = ["四字词语", "六字成语"]
        self.mode = tk.StringVar(value=self.mode_options[0])
        self.mode_menu = ttk.OptionMenu(master, self.mode, *self.mode_options, command=self.new_idiom)
        self.mode_menu.pack(pady=10)

        # 成语显示区域
        self.label_text = tk.StringVar()
        self.label = ttk.Label(master, textvariable=self.label_text, font=('calibri', 12), background='lightblue')
        self.label.pack(pady=10)

        # 输入框
        self.entry = ttk.Entry(master, font=('calibri', 12))
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda _: self.check_guess())

        # 提交按钮
        self.button = ttk.Button(master, text='提交', command=self.check_guess)
        self.button.pack(pady=10)

        # 分数
        self.score = 0
        self.score_label = ttk.Label(master, text=f'分数: {self.score}', font=('calibri', 12), background='lightblue')
        self.score_label.pack(pady=10)

        # 倒计时
        self.timer_label = ttk.Label(master, text="剩余时间: 30s", font=('calibri', 12), background='lightblue')
        self.timer_label.pack(pady=10)

        self.time_limit = 30  # 默认时间限制为30秒
        self.time_left = self.time_limit
        self.timer_running = False

        self.new_idiom()

    def new_idiom(self, *_):
        mode = self.mode.get()
        difficulty = self.difficulty.get()

        # 设置词库文件和成语难度
        filename = f'{["1", "2"][self.mode_options.index(mode)]}.txt'
        self.idiom = self.get_random_idiom(filename, difficulty)
        
        # 随机选择要隐藏的字
        self.missing_char_index = random.choice([i for i, char in enumerate(self.idiom) if char.isalnum()])
        self.label_text.set(f'猜一个成语: {self.idiom[:self.missing_char_index]}_{self.idiom[self.missing_char_index + 1:]}')

        # 清空输入框
        self.entry.delete(0, tk.END)

        # 重置计时器
        self.time_left = self.time_limit
        self.timer_label.config(text=f"剩余时间: {self.time_left}s")
        if not self.timer_running:
            self.start_timer()

    def get_random_idiom(self, filename, difficulty):
        with open(filename, 'r', encoding='utf-8') as f:
            idioms = [line.strip() for line in f]

        # 根据难度调整成语的选择
        if difficulty == "易":
            idioms = [i for i in idioms if len(i) == 4]  # 只选四字成语
        elif difficulty == "中":
            idioms = [i for i in idioms if len(i) == 5]
        elif difficulty == "难":
            idioms = [i for i in idioms if len(i) > 5]  # 选难度较大的成语

        return random.choice(idioms)

    def start_timer(self):
        self.timer_running = True
        self.countdown()

    def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"剩余时间: {self.time_left}s")
            self.master.after(1000, self.countdown)
        else:
            self.time_left = 0
            self.timer_label.config(text="时间到！")
            self.check_guess()

    def check_guess(self):
        guess = self.entry.get()

        # 判断是否正确
        if guess == self.idiom[self.missing_char_index]:
            self.score += 10
            messagebox.showinfo("结果", f'恭喜你，你猜对了！')
        else:
            self.score -= 5
            messagebox.showinfo("结果", f'很遗憾，你猜错了。正确答案是："{self.idiom[self.missing_char_index]}"')

        # 更新分数显示
        self.score_label.config(text=f'分数: {self.score}')

        # 生成新成语
        self.new_idiom()

root = tk.Tk()
my_gui = GuessIdiom(root)
root.mainloop()
