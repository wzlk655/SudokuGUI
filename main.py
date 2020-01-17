from tkinter import *
from tkinter import messagebox
import os
import random
import copy

class SudokuGUI:
    def __init__(self, num):
        self.num = num

        window =Tk()
        window.geometry('480x300')
        window.title("数独游戏")

        self.identry = Entry(window, justify='center', textvariable=StringVar())
        self.identry["state"]=DISABLED
        self.identry.pack()

        frame =Frame(window)
        frame.pack()
        # frame.grid(row=0,column=0,sticky=NSEW)

        self.cells=[] #数独空缺口
        for i in range(9):
            self.cells.append([])
            for j in range(9):
                self.cells[i].append(StringVar())

        self.entries=[]
        for i in range(9):
            self.entries.append([])
            for j in range(9):
                entry=Entry(frame,width=2,justify=RIGHT,textvariable=self.cells[i][j])
                entry.grid(row=i,column=j,sticky=NSEW)
                self.entries[i].append(entry)
        Button(window,text="上一个",command=self.prev).pack(fill=X)
        Button(window,text="提交",command=self.validate).pack(fill=X)
        Button(window,text="下一个",command=self.next).pack(fill=X)
        # Button(window,text="上一个",command=self.validate).grid(row=1,column=0,sticky=NS)
        # Button(window,text="验证",command=self.validate).grid(row=2,column=0,sticky=NS)
        # Button(window,text="下一个",command=self.validate).grid(row=3,column=0,sticky=NS)

        # 生成数独
        os.system("sudoku.exe -c "+str(self.num))
        with open("sudoku.txt", "r") as f:
             sudokus=f.read()
        sudokus=sudokus.split("\n\n")
        # print(sudokus)
        sudokus=[sudoku.split("\n") for sudoku in sudokus]  # 注意列表推导式的顺序
        # print(sudokus)
        for i in range(len(sudokus)):
            sudokus[i] = [x.split(" ") for x in sudokus[i]]
        # print(sudokus)
        self.sudokus = sudokus
        for sudoku in self.sudokus:
            # 挖空
            for block in range(9):
                row=block//3
                column=block%3
                sp=random.sample(range(0,9),2)
                for pos in range(9):
                    if pos in sp:
                        bias_x=pos//3
                        bias_y=pos%3
                        sudoku[row*3+bias_x][column*3+bias_y]=""

            space=random.sample(range(81),random.randint(30,42))
            for i in range(81):
                if(i in space):
                    sudoku[i//9][i%9]=""
        self.raw_sudokus=copy.deepcopy(sudokus)  #用来确定哪些格子只读

        self.index=-1
        self.next()
        window.mainloop()

    def prev(self):
        self.sudokus[self.index]=[[x.get() \
                   for x in self.cells[i]] for i in range(9)]  # 存储当前的数独信息
        self.index=(self.index-1+self.num)%self.num

        self.display()  

    def next(self):
        if self.index != -1:
            self.sudokus[self.index]=[[x.get() \
                    for x in self.cells[i]] for i in range(9)]  # 存储当前的数独信息
        self.index=(self.index+1)%self.num

        self.display()

    def display(self):
        sudoku=self.sudokus[self.index]
        # 刷新显示序号
        self.identry["state"]=NORMAL
        self.identry.delete(0,END)
        self.identry.insert(0,str(self.index+1))
        self.identry["state"]=DISABLED
        for i in range(9):
            for j in range(9):
                self.entries[i][j]["state"]=NORMAL
                self.entries[i][j].delete(0,END)
                self.entries[i][j].insert(0,sudoku[i][j])
                if self.raw_sudokus[self.index][i][j]!="":
                    self.entries[i][j]["state"]=DISABLED  #必须使用这种类似字典的方式而不是直接x.属性=xxx

    def validate(self):
        values = [[x.get() \
                   for x in self.cells[i]] for i in range(9)]
        for i in range(9):
            for element in values[i]:
                if not element.isdigit():
                    messagebox.showerror("Invalid Values","请检查填写，有未填或非数字！")
                    return
                elif not 1<=int(element)<=9:
                    messagebox.showerror("Invalid Values","请保证数字在1-9范围内")
                    return
            if len(set(values[i]))!=9:  # 检查行
                messagebox.showerror("Wrong Answer","请检查结果！")
                return
        for i in range(9):  # 检查列
            if len(set([values[line][i] for line in range(9)]))!=9:
                messagebox.showerror("Wrong Answer","请检查结果！")
                return
        for block in range(9):
            row=block//3
            column=block%3
            if len(set([values[row*3+pos//3][column*3+pos%3] for pos in range(9)]))!=9:
                messagebox.showerror("Wrong Answer","请检查结果！")
                return
        messagebox.showinfo("结果","恭喜正确！")

class ChooseNumber:
    def __init__(self):
        window =Tk()
        window.geometry('360x180')
        window.title("请输入生成数独数量")

        text = StringVar()
        entry = Entry(window, textvariable=text)
        entry.pack()

        btn = Button(window, text="生成", command=self.getNum)
        btn.pack()

        self.window=window
        self.text=text

        window.mainloop()

    def getNum(self):
        try:
            num=int(self.text.get())
            if num>=1 and num<=1000000:
                self.window.destroy()
            else:
                messagebox.showerror("输入非法","请输入1-1000000的数字！")
        except:
            messagebox.showerror("输入非法","请输入1-1000000的数字！")
        SudokuGUI(num)
        return


if __name__ == "__main__":
    ChooseNumber()