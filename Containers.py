"""Контейнеры"""

from Tools import partial

from tkinter import Frame, Button, SOLID, LEFT, X, Y

class ScrollableContainer(Frame):
    """Прокручиваемый контейнер"""

class NotebookContainer(Frame):
    """Многостраничный контейнер"""

    def new(self) -> int:
        """Создать новую страницу | Возвращает индекс страницы"""

        frame = dict()
        frame["ButtonOut"] = Frame(self.buttons, bd=1, relief=SOLID, height=self.h) # Контейнер кнопки страницы в меню
        frame["Id"] = self.key # Идентификатор страницы
        frame["Name"] = str(frame["Id"]) # Имя страницы
        frame["Frame"] = Frame(self.workplace) # Контейнер, представляющий собой страницу
        frame["Frame"].place(x=0, y=0, relw=1, relh=1)
        frame["Open"] = partial(self.__open__, frame) # Функция открытия страницы (реализуется как открытие страницы по её словарю, т.к. функция открытия по индексу использует несозданные данные)
        frame["OpenFunctions"] = [] # Функции, выполняемые вместе с открытием страницы
        frame["CloseFunctions"] = [] # Функции, выполняемые вместе с закрытием страницы
        frame["Button"] = Button(frame["ButtonOut"], highlightthickness=0, text=frame["Name"],
                                 command=frame["Open"]) # Сама кнопка страницы
        frame["Width"] = frame["Button"].winfo_reqwidth() + 2 # Ширина кнопки страницы
        frame["Button"].place(x=0, y=0, w=frame["Width"] - 2, h=self.h - 2)
        frame["ButtonOut"].configure(width=frame["Width"])
        if len(self.pages) != 0:
            frame["Separator"] = self.__create_separator__()
        else:
            frame["Separator"] = None
        frame["ButtonOut"].pack(side=LEFT)

        # События прокручивания над кнопками
        frame["Button"].bind('<Button-4>', self.__scroll__)
        frame["Button"].bind('<Button-5>', self.__scroll__)
        frame["ButtonOut"].bind('<Button-4>', self.__scroll__)
        frame["ButtonOut"].bind('<Button-5>', self.__scroll__)

        frame["Open"]() # Открыть созданную страницу
        self.pages[frame["Id"]] = frame # Добавление страницы в хранилище
        self.key += 1 # Страница создана
        self.__width__()
        self.__control__()
        self.__replace__()
        return frame["Id"]

    def __replace__(self):
        """Переразмещение внутреннего пространства с учётом изменения ширины и координат"""
        self.buttons.place_forget()
        self.buttons.place(x=self.x, y=0, w=self.w, h=self.h)
        self.spl.lift()
        self.spr.lift()

    def __scroll__(self, event):
        """Событие прокручивания кнопок"""
        if event.num == 4:
            self.x += 20
            if self.x > 0:
                self.x = 0
        elif event.num == 5:
            self.x -= 20
            if self.x + self.w < self.menu.winfo_width():
                self.x = self.menu.winfo_width() - self.w
        else:
            raise
        self.__width__()
        self.__control__()
        self.__replace__()

    def __width__(self):
        """Вычисление ширины внутреннего пространства"""
        self.w = 0
        for i in self.pages:
            self.w += self.pages[i]["Width"]
        self.w += self.sep

    def __control__(self):
        """Контроль не вылета кнопок из границ виджета"""
        if self.w - 2 > self.menu.winfo_width():
            if self.x > -1:
                self.x = -1
            elif self.menu.winfo_width() + 2 > self.w + self.x:
                self.x = self.menu.winfo_width() + 2 - self.w
        else:
            if self.x != -1:
                self.x = -1

    def __open__(self, frame):
        """Событие - Открыть страницу"""
        if not self.now is None:
            self.pages[self.now]["Button"].configure(bg="#D7D7D7")
        frame["Button"].configure(bg=self.activebg)
        frame["Frame"].lift()
        for i in frame["OpenFunctions"]:
            i()
        self.now = frame["Id"]

    def __init__(self, master, activebg="#00FF00", menu_h=32, **args):
        """Инициализация"""
        super().__init__(master, **args)

        # Специальные свойства
        self.pages = {} # Словарь страниц, где ключом является значение self.key в момент создания страницы
        self.key = 0  # Количество уже созданных страниц
        self.now = None  # Текущая страница
        self.w = 0  # Ширина строки меню
        self.x = 0  # Координата строки меню
        self.sep = 0  # Количество разделителей в строке меню
        self.h = menu_h # Высота строки меню

        # Свойства стиля
        self.activebg = activebg # Background

        # Внутреннее пространство виджета
        self.menu = Frame(self) # Заменить на прокручиваемый контейнер, после реализации # Внутри находится self.buttons, который и ездит туда-сюда
        self.menu.place(x=0, y=0, relw=1, h=self.h)
        self.buttons = Frame(self.menu) # Строка меню, в которой находятся кнопки
        self.buttons.place(x=self.x, y=0, w=self.w, relh=1)
        self.spl = Frame(self.menu, bg="#000000") # Левый ограничитель в виде чёрной полоски
        self.spl.place(x=0, y=0, w=1, relh=1)
        self.spr = Frame(self.menu, bg="#000000") # Правый ограничитель в виде чёрной полоски
        self.spr.place(relx=1, x=-1, y=0, w=1, relh=1)
        self.workplace = Frame(self) # Рабочее пространство, содержащее страницы
        self.workplace.place(x=0, y=self.h + 1, relw=1, relh=1, h=-(self.h + 1))
        self.menu.bind('<Button-4>', self.__scroll__)
        self.menu.bind('<Button-5>', self.__scroll__)

    def __create_separator__(self):
        """Создать разделитель"""
        frame = Frame(self.buttons, width=1, height=self.h)
        frame.pack(side=LEFT)
        frame.bind('<Button-4>', self.__scroll__)
        frame.bind('<Button-5>', self.__scroll__)
        self.sep += 1
        return frame

    def rename(self, id, name):
        """Переименовать страницу"""
        self.pages[id]["Name"] = name
        self.button(id, name)

    def button(self, id, name):
        """Переименовать кнопку"""
        self.pages[id]["Button"].configure(text=name)
        self.pages[id]["Width"] = self.pages[id]["Button"].winfo_reqwidth() + 2
        self.pages[id]["Button"].place(x=0, y=0, w=self.pages[id]["Width"] - 2, h=self.h - 2)
        self.pages[id]["ButtonOut"].configure(width=self.pages[id]["Width"])
        self.__width__()
        self.__control__()
        self.__replace__()

    def delete(self, id):
        """Закрыть страницу"""
        # Выполнение функций закрытия
        for i in self.pages[id]["CloseFunctions"]:
            i()
        # Удаление элементов интерфейса страницы
        self.pages[id]["Frame"].destroy()
        if not self.pages[id]["Separator"] is None:
            self.pages[id]["Separator"].destroy()
        self.pages[id]["ButtonOut"].destroy()
        del self.pages[id]
        # Определение новой страницы
        self.now = None
        if len(self.pages) != 0:
            self.pages[max(self.pages.keys())]["Open"]()
        else:
            self.new()
        self.__width__()
        self.__control__()
        self.__replace__()

    def get(self, id):
        """Получить ссылку на страницу по индексу"""
        return self.pages[id]

    def open(self, id):
        """Открыть страницу по индексу"""
        self.pages[id]["Open"]()

    def index(self, frame):
        """Получить индекс страницы по ссылке"""
        for i in range(len(self.pages)):
            if self.pages[i] is frame:
                return i
        raise ValueError

class PanelContainer(Frame):
    """Панельный контейнер"""

class StretchableContainer(Frame):
    """Протягиваемый внутри контейнер"""

class TableGridContainer(Frame):
    """Табличный контейнер"""

class FramedContainer(Frame):
    """Простой контейнер"""

    def __init__(self, master, **b):
        """Инициализация"""
        super().__init__(master, **b)

    def add(self, Arg, *other, **args):
        """Добавить виджет"""
        self.widget = Arg(self, *other, **args)

    def place(self, padding=0, **args):
        """Метод place"""
        super().place(**args)
        self.widget.place(x=padding, y=padding, w=-2 * padding, h=-2 * padding, relw=1, relh=1)