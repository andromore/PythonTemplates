"""Калькулятор"""
from Containers import NotebookContainer, FramedContainer
from Windows import Window
from Tools import partial

from tkinter import SOLID, Entry, Menu, Button, INSERT, END

class CalculatorManager:
    """Функционал калькулятора"""

    def __init__(self, constants, functions, operators):
        """Инициализация"""
        self.constants = constants
        self.functions = functions
        self.operators = operators

    def __type(self, value: str):
        """Получить считаемое значение"""
    
    def __calculate(self, expression: list) -> str:
        """Отработка готового выражения"""

    def __parse(self, text: str) -> list:
        """Парсер"""

    def __call__(self, text: str) -> str:
        """Обработчик"""
        string = text.replace("  ", " ").lstrip().rstrip()
        return self.__calculate(self.__parse(string))

class CalculatorApp(Window):
    """Калькулятор"""

    def __command__(self, master, name, command, row, column, width=None, height=None):
        """Создание командной кнопки"""
        i = FramedContainer(master, relief=SOLID, bd=1)
        i.add(Button, highlightthickness=0, text=name, command=command)
        i.place(x=2 * self.a * column + 2 * column, y=2 * self.a * row + 2 * row,
                w=2 * self.a + 1 if not width else width, h=2 * self.a + 1 if not height else height)

    def __insert__(self, master, name, text, row, column, width=None, height=None):
        """Создание текстовой кнопки"""
        self.__command__(master, name, partial(self.entry.insert, INSERT, text), row, column, width, height)

    def page0(self):
        """Страница меню -0-"""
        id = self.book.new()
        page = self.book.get(id)
        self.book.rename(id, "Простой")
        self.__insert__(page["Frame"], ",", ",", 3, 1)
        self.__insert__(page["Frame"], "1", "1", 2, 1)
        self.__insert__(page["Frame"], "4", "4", 1, 1)
        self.__insert__(page["Frame"], "7", "7", 0, 1)
        self.__insert__(page["Frame"], "0", "0", 3, 2)
        self.__insert__(page["Frame"], "2", "2", 2, 2)
        self.__insert__(page["Frame"], "5", "5", 1, 2)
        self.__insert__(page["Frame"], "8", "8", 0, 2)
        self.__insert__(page["Frame"], ".", ".", 3, 3)
        self.__insert__(page["Frame"], "3", "3", 2, 3)
        self.__insert__(page["Frame"], "6", "6", 1, 3)
        self.__insert__(page["Frame"], "9", "9", 0, 3)
        self.__insert__(page["Frame"], "+", " + ", 0, 0)
        self.__insert__(page["Frame"], "-", " - ", 1, 0)
        self.__insert__(page["Frame"], "×", " × ", 2, 0)
        self.__insert__(page["Frame"], "÷", " ÷ ", 3, 0)
        self.__insert__(page["Frame"], "^", " ^ ", 0, 4)
        self.__insert__(page["Frame"], "log", "log(,)", 1, 4)
        self.__insert__(page["Frame"], "", "", 2, 4)
        self.__insert__(page["Frame"], "", "", 3, 4)
        self.__insert__(page["Frame"], "(", " (", 0, 5)
        self.__insert__(page["Frame"], "sin", "sin()", 1, 5)
        self.__insert__(page["Frame"], "asin", "asin()", 2, 5)
        self.__insert__(page["Frame"], "π", " π ", 3, 5)
        self.__insert__(page["Frame"], ")", ") ", 0, 6)
        self.__insert__(page["Frame"], "cos", "cos()", 1, 6)
        self.__insert__(page["Frame"], "acos", "acos()", 2, 6)
        self.__insert__(page["Frame"], "e", " e ", 3, 6)

    def page1(self):
        """Страница меню -1-"""
        id = self.book.new()
        page = self.book.get(id)
        self.book.rename(id, "Логический")

    def page2(self):
        """Страница меню -2-"""
        id = self.book.new()
        page = self.book.get(id)
        self.book.rename(id, "Сложный")

    def __init__(self, root, id):
        """Инициализация"""
        super().__init__(root)
        self.id = id
        self.app = root.app
        self.title("OfficeRu Калькулятор")
        self.resizable(False, False)
        self.geometry("373x295")
        self.protocol("WM_DELETE_WINDOW", partial(self.app.wm.close, self.id))

        """Графический интерфейс"""
        self.a = 25
        widget = FramedContainer(self, bd=1, relief=SOLID)
        widget.add(Entry)
        widget.place(x=5, y=5, w=self.a * 12 + 11, h=self.a * 2 + 1)
        self.entry = widget.widget
        self.book = NotebookContainer(self, menu_h=self.a)
        self.book.place(x=5, y=self.a * 2 + 7, relw=1, w=-10, relh=1, h=-(self.a * 2 + 12))
        widget = FramedContainer(self, bd=1, relief=SOLID)
        widget.add(Button, text="↵",
                   highlightthickness=0)
        widget.place(x=5 + self.a * 12 + 11 + 1, y=5, w=self.a * 2 + 1, h=self.a * 2 + 1)
        self.page0()

        """Меню окна"""
        self.menu = Menu(self, tearoff=0)

        """Меню [Файл]"""
        self.menu.file = Menu(self.menu, tearoff=0)
        self.menu.file.add_command(label="Новое окно", command=self.app.am.calculator)
        self.menu.file.add_separator()
        self.menu.file.add_command(label="Закрыть окно")
        self.menu.add_cascade(label="Файл", menu=self.menu.file)

        """Меню [Файл > Запустить]"""
        self.menu.file.apps = Menu(self.menu.file, tearoff=0)
        self.menu.file.apps.add_command(label="Калькулятор", command=self.app.am.calculator)
        self.menu.file.insert_cascade(12, label="Запустить", menu=self.menu.file.apps)

        """Меню [Правка]"""
        self.menu.edit = Menu(self.menu, tearoff=0)
        self.menu.edit.add_command(label="Поиск")
        self.menu.edit.add_command(label="Заменить")
        self.menu.add_cascade(label="Правка", menu=self.menu.edit)

        """Меню [Правка > Вставить]"""
        self.menu.edit.insert = Menu(self.menu.edit, tearoff=0)
        self.menu.edit.insert.add_command(label="Время")
        self.menu.edit.insert.add_command(label="Дата")
        self.menu.edit.insert.add_command(label="Цвет")
        self.menu.edit.add_cascade(label="Вставить", menu=self.menu.edit.insert)

        """Меню [Инструменты]"""
        self.menu.edit.instrument = Menu(self.menu.edit, tearoff=0)
        self.menu.edit.add_cascade(label="Инструмент", menu=self.menu.edit.instrument)

        """Меню [Вид]"""
        self.menu.view = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Вид", menu=self.menu.view)

        """Меню [Настройки]"""
        self.menu.sett = Menu(self.menu, tearoff=0)
        self.menu.sett.add_command(label="Типы файлов")
        self.menu.add_cascade(label="Настройки", menu=self.menu.sett)

        self.menu.add_command(label="Помощь")
        self.configure(menu=self.menu)
