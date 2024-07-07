"""Базовые виджеты"""

from Tools import partial, passing

from tkinter import *

class ImageButtonWidget(Button):
    """Кнопка с изображением"""

    def __init__(self, master, image=None, **args):
        """Инициализация"""
        if image is not None:
            self.image = PhotoImage(file=image)
            args["image"] = self.image
        super().__init__(master, **args)

class ImageWidget(Label):
    """Изображение"""

    def __init__(self, master, image=None, **args):
        """Инициализация"""
        if image is not None:
            self.image = PhotoImage(file=image)
            args["image"] = self.image
        super().__init__(master, **args)

class BalloonWidget(Menu):
    """Подсказка""" # Помнится, были баги, надо тестировать

    def __init__(self, root, text="", delay=1, **args):
        """Инициализация"""
        super().__init__(root, **args)

        self.delay = delay * 1000

        self.label = Label(self, text=text)
        self.label.pack()
        self.master.bind('<Enter>', self.__post__)
        self.master.bind('<Leave>', self.__unpost__)
        self.master.bind('<Motion>', self.__unpost__)
        self.master.bind('<Button>', self.__unpost__)
        self.master.bind('<Key>', self.__unpost__)

    def __post__(self, *event):
        """Событие"""
        self.after(self.delay, partial(self.post, self.master.winfo_rootx(),
                                       self.master.winfo_rooty() - self.winfo_reqheight()))

    def __unpost__(self, *event):
        """Событие"""
        self.unpost()

class PopupMenuWidget(Menu):
    """Всплывающее меню""" # Работает также, как и обычное меню

    def __init__(self, root, **args):
        """Инициализация"""
        super().__init__(root, **args)
        self.master.bind('<Button-3>', self.__post__)
        self.bind('<Leave>', self.__unpost__)

    def __post__(self, *event):
        """Событие"""
        self.post(event[0].x_root, event[0].y_root)

    def __unpost__(self, *event):
        """Событие"""
        self.unpost()

class TextWidget(Frame):
    """Текстовый виджет"""

    def __init__(self, root, font=None, tab="\t", **kwargs):
        """Инициализация"""
        super().__init__(root, **kwargs)

        self.line = None
        self.tab = tab

        self.widget = Frame(self, bg="#000000", bd=1)
        self.x = Frame(self.widget, bd=1, relief=RAISED)
        self.y = Frame(self.widget, bd=1, relief=RAISED)
        self.xscroll = Scrollbar(self.x, orient=HORIZONTAL, relief=FLAT, bd=0)
        self.yscroll = Scrollbar(self.y, orient=VERTICAL, relief=FLAT, bd=0)
        self.lines = Text(self.widget, highlightthickness=0, relief=FLAT, wrap=NONE, spacing1=1, spacing3=1, spacing2=1,
                          font=font)
        self.text = Text(self.widget, highlightthickness=0, relief=FLAT, wrap=NONE, spacing1=1, spacing3=1, spacing2=1,
                         font=font)
        self.special = Button(self.widget, highlightthickness=0)

        def multiscrolling(self, *args):
            """Прокручивать текст и строки одновременно"""
            self.lines.yview(*args)
            self.text.yview(*args)

        def xscrolling(self, *args):
            """Прокручивать по горизонтали"""
            self.xscroll.set(*args)
            self.text.xview('moveto', args[0])

        def yscrolling(self, *args):
            """Прокручивать по вертикали"""
            self.yscroll.set(*args)
            multiscrolling(self, 'moveto', args[0])

        self.yscroll.config(command=partial(multiscrolling, self))
        self.xscroll.config(command=self.text.xview)
        self.lines.configure(yscrollcommand=partial(yscrolling, self))
        self.text.configure(yscrollcommand=partial(yscrolling, self), xscrollcommand=partial(xscrolling, self))

        self.widget.place(x=0, y=0, relw=1, relh=1)
        self.x.place(x=0, rely=1, y=-22, w=-23, relw=1, h=22)
        self.y.place(relx=1, x=-22, y=0, w=22, relh=1, h=-23)
        self.xscroll.place(x=0, y=0, relw=1, relh=1)
        self.yscroll.place(x=0, y=0, relw=1, relh=1)
        self.lines.place(x=0, y=0, w=20, relh=1, h=-23)
        self.text.place(x=21, y=0, relw=1, w=-44, relh=1, h=-23)
        self.special.place(relx=1, x=-22, rely=1, y=-22, w=22, h=22)

        self.text.bind('<<Modified>>', self.__state__)
        self.text.bind('<KeyRelease>', self.__insert__)
        self.text.bind('<ButtonRelease>', self.__insert__)
        self.text.bind('<Control-Key-a>', self.__ctrl_a__)
        self.text.bind('<Control-Key-A>', self.__ctrl_a__)

        self.lines.tag_config("line", background="#00FF00")

        self.delete = self.text.delete
        self.insert = self.text.insert
        self.get = self.text.get
        self.clear = partial(self.delete, "1.0", END)
        self.bind = self.text.bind
        self.update = self.__state__

        self.__insert__()

    def __state__(self, *event):
        """Событие <<Modified>>"""
        lines = int(self.text.index(END).split(".")[0]) - 1
        if self.line != lines: # Если количество строк отличается, то надо пересобрать нумерацию строк
            text = "" # Можно придумать и побыстрее, но это работает
            for i in range(1, lines):
                text += str(i).rjust(len(str(lines))) + "\n"
            text += str(lines).rjust(len(str(lines)))
            self.lines.configure(state=NORMAL)
            self.lines.delete("1.0", END)
            self.lines.insert("1.0", text)
            self.lines.configure(state=DISABLED)
            if len(str(lines)) != len(str(self.line)): # Если длина нумерации увеличилась, то надо сместить границу
                self.lines.place_forget()
                self.text.place_forget()
                self.lines.place(x=0, y=0, w=(len(str(lines)) + 1) * 10, relh=1, h=-23)
                self.text.place(x=(len(str(lines)) + 1) * 10 + 1, y=0, relw=1, w=-(len(str(lines)) + 1) * 10 - 24,
                                relh=1, h=-23)
            self.line = lines
        self.text.edit_modified(False) # Т.к. модификация текста программно считается вызывает событие повторно
        return 'break'

    def __insert__(self, *event):
        """Событие <KeyRelease> или <ButtonRelease>""" # Подсветка текущей строки
        self.__state__()
        now = self.text.index(INSERT)
        self.lines.tag_remove("line", 1.0, END)
        line = now.split(".")[0]
        self.lines.tag_add("line", str(line) + ".0", str(line) + "." + str(self.line))
        return 'break'

    def __ctrl_a__(self, *event):
        """Событие <Control-Key-a> и <Control-Key-A>""" # Событие - выделить всё
        self.text.tag_add(SEL, "1.0", END)
        return 'break'

    def __tab__(self, *event): # Вставка табуляции - по умолчанию нет в библиотеке
        """Событие <Tab>"""
        self.text.insert(INSERT, self.tab)
        self.__insert__()
        return 'break'
    
    def configure(self, font=None, tab=None, **kwargs):
        """Конфигурирование"""
        if font:
            self.lines.configure(font=font)
            self.text.configure(font=font)
        if tab:
            self.tab = tab
        if kwargs:
            self.configure(**kwargs)
            

class DebugTextWidget(Frame):
    """Текстовый виджет"""

    def multi_scrolling(self, *args):
        """Прокручивать текст и строки одновременно"""
        self.lines.yview(*args)
        self.text.yview(*args)
        
    def x_scrolling(self, *args):
        """Прокручивать по горизонтали"""
        self.x_scroll.set(*args)
        self.text.xview('moveto', args[0])
        
    def y_scrolling(self, *args):
        """Прокручивать по вертикали"""
        self.y_scroll.set(*args)
        self.multi_scrolling('moveto', args[0])

    def __init__(self, root, font=None, **kwargs):
        """Инициализация"""
        super().__init__(root, **kwargs)

        self.widget = Frame(self, bg="#000000", bd=1)
        self.x = Frame(self.widget, bd=1, relief=RAISED)
        self.y = Frame(self.widget, bd=1, relief=RAISED)
        self.x_scroll = Scrollbar(self.x, orient=HORIZONTAL, relief=FLAT, bd=0)
        self.y_scroll = Scrollbar(self.y, orient=VERTICAL, relief=FLAT, bd=0)
        self.lines = Text(self.widget, highlightthickness=0, relief=FLAT,
                          wrap=NONE, spacing1=1, spacing3=1, spacing2=1, font=font)
        self.text = Text(self.widget, highlightthickness=0, relief=FLAT, tabs="1c",
                         wrap=NONE, spacing1=1, spacing3=1, spacing2=1, font=font)
        self.special = Button(self.widget, highlightthickness=0)

        self.y_scroll.config(command=self.multi_scrolling)
        self.x_scroll.config(command=self.text.xview)
        self.lines.configure(yscrollcommand=self.y_scrolling)
        self.text.configure(yscrollcommand=self.y_scrolling, xscrollcommand=self.x_scrolling)

        self.widget.place(x=0, y=0, relw=1, relh=1)
        self.x.place(x=0, rely=1, y=-22, w=-23, relw=1, h=22)
        self.y.place(relx=1, x=-22, y=0, w=22, relh=1, h=-23)
        self.x_scroll.place(x=0, y=0, relw=1, relh=1)
        self.y_scroll.place(x=0, y=0, relw=1, relh=1)
        self.lines.place(x=0, y=0, w=20, relh=1, h=-23)
        self.text.place(x=21, y=0, relw=1, w=-44, relh=1, h=-23)
        self.special.place(relx=1, x=-22, rely=1, y=-22, w=22, h=22)

        self.line = self.text.index(END)
        self.now = self.text.index(INSERT)

        self.lines.tag_config("line", background="#00FF00")
        
    def insert(self, *event):
        now = self.text.index(INSERT)
        self.lines.tag_remove("line", 1.0, END)
        line = now.split(".")[0]
        self.lines.tag_add("line", str(line) + ".0", str(line) + "." + str(self.line))


root = Tk()
DebugTextWidget(root).place(x=0, y=0, relw=1, relh=1)
root.mainloop()