import math
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import *
import numpy as np
matplotlib.use('qt5agg')


class WorkSpace:
    fig = plt.figure()
    start = 0
    end = 0
    delta = 0
    axes_list = []
    x = []
    y = []
    x_extra = []
    y_extra = []
    frequency = []

    def __init__(self):
        self.calc = Calculations()
        self.file_f = False
        self.filename = ''

    def on_btn_click(self, event):
        if self.file_f:
            self.x, self.y = self.calc.read_file(self.filename)
            y = []
            x, y = self.calc.add_points_f(self.x, self.y)
            self.frequency = np.linspace(-(len(y) / 2), len(y) / 2, len(y))
            self.update()
            y_not_complex = list(map(np.abs, self.calc.BPF(y)))
            y_not_complex = self.invert(y_not_complex)
            savefile('output.txt', self.frequency, y_not_complex)
            self.axes_list[3].stem(y_not_complex)
        else:
            self.x, self.y = self.calc.count_function(self.start, self.end, self.delta)
            self.N = len(self.x)
            self.x_extra, self.y_extra = self.calc.add_points(self.x, self.y)
            mash_coeff = self.N/len(self.x_extra)
            step = (1/(self.x_extra[len(self.x_extra)-1] - self.x_extra[0])) * mash_coeff
            self.N = len(self.x_extra)
            self.frequency = np.arange(((-self.N/2)*step), (self.N/2)*step, step)
            self.update()
            self.yy = self.calc.BPF(self.y_extra)
            y_not_complex = list(map(np.abs, self.yy))
            y_not_complex = self.invert(y_not_complex)
            savefile('output.txt', self.frequency, y_not_complex)
            self.axes_list[3].stem(self.frequency, y_not_complex)

    def on_file_click(self, expr):
        if expr == '':
            self.filename = ''
            self.file_f = False
        else:
            self.filename = str(expr)
            self.file_f = True

    def on_start_click(self, expr):
        if expr == '':
            self.start = 0
        else:
            self.start = float(eval(expr))

    def on_end_click(self, expr):
        if expr == '':
            self.end = 0
        else:
            self.end = float(eval(expr))

    def invert(self, a):
        b = a[len(a)//2:len(a):1]
        c = a[0:len(a)//2:1]
        b = b+c
        return b

    def on_delta_click(self, expr):
        if expr == '':
            self.delta = 0
        else:
            self.delta = float(eval(expr))

    def window_settings(self):
        mng = plt.get_current_fig_manager()
        mng.set_window_title('Lab_1')
        mng.window.showMaximized()
        axbox_ = plt.axes([0.05, 0.85, 0.1, 0.03])
        self.file = TextBox(axbox_, 'Файл')
        self.file.on_submit(self.on_file_click)
        axbox = plt.axes([0.05, 0.40, 0.1, 0.03])
        self.button = Button(axbox, "Submit")
        self.button.on_clicked(self.on_btn_click)
        axbox1 = plt.axes([0.05, 0.75, 0.1, 0.03])
        self.text_box_start = TextBox(axbox1, 'Начало')
        self.text_box_start.on_submit(self.on_start_click)
        axbox2 = plt.axes([0.05, 0.65, 0.1, 0.03])
        self.text_box_end = TextBox(axbox2, 'Конец')
        self.text_box_end.on_submit(self.on_end_click)
        axbox3 = plt.axes([0.05, 0.55, 0.08, 0.03])
        self.text_box_delta = TextBox(axbox3, 'Шаг')
        self.text_box_delta.on_submit(self.on_delta_click)
        self.text_box_delta.set_val(self.delta)
        self.text_box_end.set_val(self.end)
        self.text_box_start.set_val(self.start)
        self.fig.subplots_adjust(right=0.9, left=-0.1)
        ax1 = self.fig.add_subplot(2, 3, 3)
        ax2 = self.fig.add_subplot(232)
        ax3 = self.fig.add_subplot(235)
        ax4 = self.fig.add_subplot(236)
        self.axes_list = [ax1, ax2, ax3, ax4]

    def update(self):
        for ax in self.axes_list:
            ax.clear()
        self.axes_list[0].set_title(u'График')
        self.axes_list[1].set_title(u'Квантованный график')
        self.axes_list[2].set_title(u'Дискретный график')
        self.axes_list[3].set_title(u'Результат БПФ')
        self.axes_list[3].set_xlabel('Частота')
        self.axes_list[3].set_ylabel('Магнитуда')
        for ax in self.fig.axes:
            ax.grid(True)
            if self.file_f:
                self.text_box_delta.set_val('')
                self.text_box_end.set_val('')
                self.text_box_start.set_val('')
            else:
                self.calc.count_function(self.start, self.end, self.end)
        self.axes_list[0].plot(self.x, self.y)
        self.axes_list[1].step(self.x, self.y)
        self.axes_list[1].plot(self.x, self.y)
        self.axes_list[2].stem(self.x, self.y)


class Calculations:
    def __int__(self):
        pass

    def count_function(self, start, end, delta):
        x = np.arange(start, end, delta)
        y = np.sin(2 * x) + np.cos(7 * x)
        return x, y

    def BPF(self, a):
        if(len(a) == 1):
            return a
        else:
            y = []
            b = []
            c = []
            y1 = []
            y2 = []
            for i in range(0, len(a)//2, 1):
                wn = complex((np.cos((-2 * i * np.pi) / len(a))), (np.sin((-2*i * np.pi) / len(a))))
                b.append(a[i]+a[i+len(a)//2])
                c.append((a[i] - a[i+len(a)//2])*wn)
            y1 = self.BPF(b)
            y2 = self.BPF(c)
            for j in range(0, len(a)//2):
                y.insert(2*j, y1[j])
                y.insert(2*j+1, y2[j])
            return y

    def read_file(self, filename='data.txt'):
        x = []
        y = []
        with open(filename) as file:
            a = True
            while a:
                file_line = file.readline().rstrip()
                if not file_line:
                    print("End Of File")
                    a = False
                else:
                    tmp = list(map(float, file_line.split('\t')))
                    x.append(tmp[0])
                    y.append(tmp[1])
            return x, y

    def add_points_f(self, x, y):
        x1 = x.copy()
        y1 = y.copy()
        near_2 = self.near_2_deg(len(x))
        for i in range(near_2 - len(x)):
            x1.append(0)
            y1.append(0)
        return x1, y1

    def add_points(self, x, y):
        near_2 = self.near_2_deg(len(x))
        x1 = np.linspace(x[0], x[len(x)-1], near_2)
        y1 = np.sin(2 * x1) + np.cos(7 * x1)
        return x1, y1

    def near_2_deg(self, n):
        i = 1
        while 2 ** i < n:
            i += 1
        return 2 ** (i)


def savefile(filename, x, y):
    with open(filename, 'w+') as f:
        for i in range(len(x)):
            f.write(str(x[i]) + '\t' + str(y[i]) + '\n')


def main():
    workspace = WorkSpace()
    workspace.window_settings()
    plt.show()


if __name__ == '__main__':
    main()
