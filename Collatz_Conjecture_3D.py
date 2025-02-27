import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D


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
        self.root.title("Collatz猜想三维可视化")

        # 创建输入组件
        self.create_inputs()

        # 初始化图表
        self.fig = Figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # 创建结果显示区域
        self.result_label = tk.Label(self.root, text="结果将显示在这里", fg="blue")
        self.result_label.pack(pady=10)

        # 存储三维坐标的字典
        self.points = {}

    def create_inputs(self):
        # 三维绘图输入
        frame_3d = tk.Frame(self.root)
        frame_3d.pack(pady=5)
        tk.Label(frame_3d, text="最大数字:").pack(side=tk.LEFT)
        self.entry_max = tk.Entry(frame_3d, width=10)
        self.entry_max.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_3d, text="三维绘图", command=self.plot_3d).pack(side=tk.LEFT)

        # 清除按钮
        tk.Button(self.root, text="清除图表", command=self.clear_plot).pack(pady=5)

    def generate_spiral_point(self, n):
        # 螺旋参数
        theta = n * np.pi / 4  # 角度随n增加
        r = 0.1 * np.sqrt(n)  # 半径随n增大
        z = n * 0.2  # 高度随n增加
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return (x, y, z)

    def plot_3d(self):
        try:
            max_num = int(self.entry_max.get())
            if max_num <= 0:
                raise ValueError
        except:
            messagebox.showerror("错误", "请输入有效的正整数")
            return

        self.ax.clear()
        self.points = {}

        # 生成所有点的坐标
        for n in range(1, max_num + 1):
            coord = self.generate_spiral_point(n)
            self.points[n] = coord
            self.ax.scatter(*coord, c='b', marker='o')

        # 绘制连接线段
        for n in range(1, max_num + 1):
            # 规则a: 大数是小数的两倍
            if 2 * n in self.points:
                self.ax.plot(*zip(self.points[n], self.points[2 * n]), c='g', alpha=0.3)

            # 规则b: 大数是小数的三倍加1
            m = (n - 1) / 3
            if m.is_integer() and m > 0 and m in self.points:
                self.ax.plot(*zip(self.points[int(m)], self.points[n]), c='r', alpha=0.3)

        # 设置坐标轴标签
        self.ax.set_xlabel('X轴')
        self.ax.set_ylabel('Y轴')
        self.ax.set_zlabel('Z轴')
        self.ax.set_title(f'数字1-{max_num}的三维螺旋分布')
        self.canvas.draw()

        self.result_label.config(text=f"已绘制1到{max_num}的三维分布图\n"
                                      f"绿色线段：大数是小数的两倍\n"
                                      f"红色线段：大数是小数的三倍加一")

    def clear_plot(self):
        self.ax.clear()
        self.ax.set_xlabel('X轴')
        self.ax.set_ylabel('Y轴')
        self.ax.set_zlabel('Z轴')
        self.canvas.draw()
        self.result_label.config(text="结果将显示在这里")


if __name__ == "__main__":
    root = tk.Tk()
    app = CollatzPlotter(root)
    root.mainloop()