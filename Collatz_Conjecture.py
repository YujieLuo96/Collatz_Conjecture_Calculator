import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def generate_collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
        sequence.append(n)
    x = list(range(len(sequence)))
    return x, sequence, max(sequence)


class CollatzPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Collatz猜想图表")

        # 创建输入组件
        self.create_inputs()

        # 初始化图表
        self.fig = Figure(figsize=(8, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # 创建结果显示区域
        self.result_label = tk.Label(self.root, text="结果将显示在这里", fg="blue")
        self.result_label.pack(pady=10)

    def create_inputs(self):
        # 单个数字输入
        frame_single = tk.Frame(self.root)
        frame_single.pack(pady=5)
        tk.Label(frame_single, text="单个数字:").pack(side=tk.LEFT)
        self.entry_single = tk.Entry(frame_single, width=10)
        self.entry_single.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_single, text="绘制", command=self.plot_single).pack(side=tk.LEFT)

        # 范围输入
        frame_range = tk.Frame(self.root)
        frame_range.pack(pady=5)
        tk.Label(frame_range, text="范围从:").pack(side=tk.LEFT)
        self.entry_start = tk.Entry(frame_range, width=5)
        self.entry_start.pack(side=tk.LEFT)
        tk.Label(frame_range, text="到").pack(side=tk.LEFT)
        self.entry_end = tk.Entry(frame_range, width=5)
        self.entry_end.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_range, text="绘制范围", command=self.plot_range).pack(side=tk.LEFT)

        # 清除按钮
        tk.Button(self.root, text="清除图表", command=self.clear_plot).pack(pady=5)

    def validate_input(self, input_str, is_range=False):
        try:
            num = int(input_str)
            if num <= 0:
                return False
            return num
        except ValueError:
            return False

    def plot_single(self):
        input_str = self.entry_single.get()
        num = self.validate_input(input_str)
        if not num:
            messagebox.showerror("错误", "请输入有效的正整数")
            return
        x, y, max_value = generate_collatz_sequence(num)
        self.ax.plot(x, y, label=f'n={num}')
        self.ax.legend()
        self.canvas.draw()
        self.result_label.config(text=f"数字 {num} 的序列最大值为: {max_value}")

    def plot_range(self):
        start = self.validate_input(self.entry_start.get())
        end = self.validate_input(self.entry_end.get())

        if not start or not end or start > end:
            messagebox.showerror("错误", "请输入有效的正整数范围")
            return

        max_sequence_value = -1
        max_sequence_number = -1

        for n in range(start, end + 1):
            x, y, current_max = generate_collatz_sequence(n)
            if current_max > max_sequence_value:
                max_sequence_value = current_max
                max_sequence_number = n
            self.ax.plot(x, y, label=f'n={n}')

        self.ax.legend()
        self.canvas.draw()
        self.result_label.config(
            text=f"范围 [{start}, {end}] 中，数字 {max_sequence_number} 的序列最大值最大，为: {max_sequence_value}")

    def clear_plot(self):
        self.ax.clear()
        self.ax.set_xlabel("步骤次数")
        self.ax.set_ylabel("数值")
        self.canvas.draw()
        self.result_label.config(text="结果将显示在这里")


if __name__ == "__main__":
    root = tk.Tk()
    app = CollatzPlotter(root)
    root.mainloop()