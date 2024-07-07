"""Текстовый редактор"""

from DateTime import Date, Time
from Widgets import TextWidget, PopupMenuWidget
from Containers import NotebookContainer
from Windows import Window, DialogWindow
from Tools import partial

from urllib.request import urlopen
from tkinter import *
from tkinter.messagebox import askyesno, showerror, showwarning
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename, askopenfilename


class CopybookWidget(Frame):
    """Тетрадь"""

    def __init__(self, master, bar=True, file=True, lang=True, line=True):
        """Инициализация"""
        super().__init__(master)
        self.app = master.app
        self.book = NotebookContainer(self)
        self.status = {"bar": False, "file": False, "lang": False, "line": False}
        self.bar = Frame(self, bd=1, relief=SOLID)
        self.file = Button(self.bar, highlightthickness=0)
        self.file.sep = Frame(self.bar, width=1, bg="#000000")
        self.line = Button(self.bar, highlightthickness=0)
        self.line.sep = Frame(self.bar, width=1, bg="#000000")
        self.lang = Button(self.bar, highlightthickness=0, text="LANG")
        self.lang.sep = Frame(self.bar, width=1, bg="#000000")
        self.sep = Button(self.bar, highlightthickness=0)
        self.__status__(bar=bar, file=file, lang=lang, line=line)

    def new(self):
        """Создание новой страницы -> Возвращает индекс страницы"""
        index = self.book.new()
        page = self.book.get(index)
        page["TextWidget"] = TextWidget(page["Frame"])
        page["TextWidget"].place(x=0, y=0, relw=1, relh=1)

        def func(*event):
            page["Saved"] = False
        page["TextWidget"].bind("<Key>", func)
        
        """Сначала разобраться с событиями - иначе баги + они и так есть
        def func(*event):
            self.line.configure(text=str(page["TextWidget"].text.index(INSERT)))
        page["TextWidget"].bind("<KeyRelease>", func)
        page["TextWidget"].bind("<ButtonRelease>", func)
        """
        
        self.book.rename(index, "Без имени " + str(page["Id"]))
        self.file.configure(text=page["Name"])
        page["OpenFunctions"].append(lambda: self.file.configure(text=page["Name"]))
        page["Saved"] = True
        page["Button"].configure(text=page["Name"].split("/")[-1])

        """Меню действий с конкретной страницей"""
        page["PopupMenu"] = PopupMenuWidget(page["Button"], tearoff=0)
        page["PopupMenu"].add_command(label="Сохранить",
                                      command=partial(self.master.__save__, page["Id"]))
        page["PopupMenu"].add_command(label="Сохранить как",
                                      command=partial(self.master.__save_as__, page["Id"]))
        page["PopupMenu"].add_separator()
        page["PopupMenu"].add_command(label="Переименовать",
                                      command=partial(self.master.__rename__, page["Id"]))
        page["PopupMenu"].add_separator()
        page["PopupMenu"].add_command(label="Закрыть",
                                      command=partial(self.master.__close__, page["Id"]))

    def configure(self, **args):
        """Редактирование свойств"""
        if "bar" in args or "line" in args or "file" in args or "lang" in args:
            self.__status__(**args)

    def __status__(self, **args):
        """Строка состояния"""
        self.sep.pack_forget()
        if args["bar"] != self.status["bar"]:
            if args["bar"]:
                self.book.place_forget()
                self.book.place(x=0, y=0, relw=1, relh=1, h=-23)
                self.bar.place(x=0, rely=1, y=-22, relw=1, h=22)
            else:
                self.bar.place_forget()
                self.book.place_forget()
                self.book.place(x=0, y=0, relw=1, relh=1)
            self.status["bar"] = args["bar"]
        if args["file"] != self.status["file"]:
            if args["file"]:
                self.file.pack(side=LEFT, fill=Y)
                self.file.sep.pack(side=LEFT, fill=Y)
            else:
                self.file.pack_forget()
                self.file.sep.pack_forget()
            self.status["file"] = args["file"]
        if args["line"] != self.status["line"]:
            if args["line"]:
                self.line.pack(side=RIGHT, fill=Y)
                self.line.sep.pack(side=RIGHT, fill=Y)
            else:
                self.line.pack_forget()
                self.line.sep.pack(side=RIGHT, fill=Y)
            self.status["line"] = args["line"]
        if args["lang"] != self.status["lang"]:
            if args["lang"]:
                self.lang.pack(side=RIGHT, fill=Y)
                self.lang.sep.pack(side=RIGHT, fill=Y)
            else:
                self.lang.pack_forget()
                self.lang.sep.pack_forget()
            self.status["lang"] = args["lang"]
        self.sep.pack(fill=BOTH)

    def rename(self, id, name):
        """Переименовать страницу"""
        self.book.rename(id, name)
        self.book.button(id, name)
        self.file.configure(text=name)


class FileTypesWindow(DialogWindow):
    """Типы файлов"""
    
    class Dialog(DialogWindow):
        """Локальный диалоговый класс"""

        def done(self):
            """Готово"""
            if self.index:
                self.master.box.delete(self.index)
            self.master.box.insert(END, self.entry1.get() + " - " + self.entry2.get())
            self.destroy()
        
        def __init__(self, master, title, field1=None, field2=None, index=None):
            super().__init__(master)
            self.title(title)
            self.minsize(400, 200)
            self.index = index
            frame = Frame(self, bd=1, relief=SOLID, bg="#000000")
            frame.place(x=1, y=1, relw=1, h=63, w=-2)
            Button(frame, text="Название", highlightthickness=0)\
                .place(x=0, y=0, w=150, h=30)
            self.entry1 = Entry(frame, highlightthickness=0, bd=0)
            self.entry1.place(x=151, y=0, relw=1, w=-151, h=30)
            Button(frame, text="Шаблон", highlightthickness=0)\
                .place(x=0, y=31, w=150, h=30)
            self.entry2 = Entry(frame, highlightthickness=0, bd=0)
            self.entry2.place(x=151, y=31, relw=1, w=-151, h=30)
            if index:
                self.entry1.insert(0, field1)
                self.entry2.insert(0, field2)

            Frame(self, bd=1, relief=SOLID)\
                .place(x=1, relw=1, w=-2, rely=1, y=-33, h=32)
            Button(self, command=self.done, text="Готово", highlightthickness=0)\
                .place(x=2, relw=1, w=-4, rely=1, y=-32, h=30)
            frame = Frame(self, bd=1, relief=SOLID)
            frame.place(x=1, y=65, relw=1, w=-2, relh=1, h=-99)
            Button(frame, text="Подсказка", highlightthickness=0).pack(side=TOP, fill=X)
            Frame(frame, bg="#000", height=1).pack(side=TOP, fill=X)
            Label(frame, relief=RAISED, bd=1, text="Название - просто название типа файлов.\
                \nШаблон - указание на имя подходящих файлов.\
                \nК примеру:\nНазвание: \tОбычный текст\nШаблон: \t*.txt\
                \nгде * обозначает любую последовательность символов.",\
                justify=LEFT, anchor=NW, padx=5, pady=5).pack(side=TOP, fill=BOTH, expand=True)
            Frame(frame, height=1, bg="#000000").pack(side=TOP, fill=X)

    def done(self):
        """Готово"""
        types = list(self.box.get(0, END))
        for i in range(len(types)):
            types[i] = types[i].split(" - ")
        self.master.app.settings["Global"]["FileTypes"] = types
        self.destroy()

    def edit(self):
        """Изменить"""
        index = self.box.curselection()
        if index:
            self.Dialog(self, "Изменить", *self.box.get(index).split(" - "), index=index)

    def delete(self):
        """Удалить"""
        index = self.box.curselection()
        if index:
            self.box.delete(index)
    
    def __init__(self, master):
        super().__init__(master)
        self.title("Типы файлов")
        self.minsize(400, 500)

        self.box = Listbox(self, highlightthickness=0, relief=SOLID)
        self.box.place(x=1, y=1, relw=1, relh=1, w=-155, h=-2)

        for i in list(self.master.app.settings["Global"]["FileTypes"]):
            self.box.insert(END, i[0] + " - " + i[1])

        self.cancel = self.destroy
        self.add = lambda: self.Dialog(self, "Добавить")

        frame = Frame(self, bd=1, relief=SOLID, bg="#000000")
        frame.place(relx=1, x=-153, w=152, y=1, relh=1, h=-2)
        Button(frame, highlightthickness=0, text="Добавить", command=self.add,
               activebackground="#00FF00").place(x=0, y=0, w=150, h=30)
        Button(frame, highlightthickness=0, text="Изменить", command=self.edit,
               activebackground="#FFFF00").place(x=0, y=31, w=150, h=30)
        Button(frame, highlightthickness=0, text="Удалить", command=self.delete,
               activebackground="#FF0000").place(x=0, y=62, w=150, h=30)
        Button(frame, highlightthickness=0).place(x=0, y=93, w=150, relh=1, h=-155)
        Button(frame, highlightthickness=0, text="Готово", command=self.done)\
            .place(x=0, rely=1, y=-61, w=150, h=30)
        Button(frame, highlightthickness=0, text="Отмена", command=self.cancel)\
            .place(x=0, rely=1, y=-30, w=150, h=30)
    

class TextEditorApp(Window):
    """Текстовый редактор"""

    def insert_color(self):
        """Вставить дату"""
        try:
            color = askcolor()[1]
            self.__insert__(self.book.book.now, color)
        except Exception as e:
            showerror("Ошибка", "Ошибка вставки цвета: функция была отменена или вызвала внутреннюю ошибку")

    def insert_date(self):
        """Вставить дату"""
        self.__insert__(self.book.book.now, str(Date.now()))

    def insert_time(self):
        """Вставить дату"""
        self.__insert__(self.book.book.now, str(Time.now()))

    def open_web_page(self):
        """Открыть код web-страницы в новой вкладке"""
        window = DialogWindow(self)
        window.geometry("200x34")
        window.minsize(300, 34)
        window.maxsize(700, 34)
        window.title("Открыть веб-страницу")
        window.resizable(True, False)
        entry = Entry(window, relief=SOLID, bd=1, highlightthickness=0)
        entry.place(x=1, y=1, relw=1, h=32, w=-75)
        entry.insert(END, "https://")

        def run(self, window, entry):
            """Запрос"""
            try:
                self.new()
                name = entry.get()
                self.__insert__(self.book.book.now, urlopen(name).read())
                self.__rename__(self.book.book.now, name)
            except Exception as e:
                showerror("Ошибка", "Произошла ошибка: " + str(e))
            window.destroy()

        Frame(window, bg="#000000").place(relx=1, x=-73, w=72, y=1, h=32)
        Button(window, command=partial(run, self, window, entry),
               bd=1, highlightthickness=0, text="Открыть").place(relx=1, x=-72, w=70, y=2, h=30)

    def save_all(self):
        """Сохранить всё"""
        for id in self.book.book.pages.keys():
            self.__save__(id)

    def open(self):
        """Открыть файл в новой странице"""
        self.new()
        self.__open__(self.book.book.now)

    def __open__(self, id):
        """Открыть файл"""
        name = askopenfilename(filetypes=self.app.settings["Global"]["FileTypes"],
                               initialdir=self.app.settings["Global"]["HomeDir"])
        if name:
            with open(name, mode="r") as file:
                text = file.read()
            page = self.book.book.get(id)
            self.__rename__(id, name)
            page["Saved"] = True
            page["TextWidget"].clear()
            page["TextWidget"].insert("1.0", text)
            if text[-1] == "\n":
                page["TextWidget"].delete(END + "-2c")
            page["TextWidget"].update()
        else:
            showwarning(message="Вы не указали файл.")

    def __insert__(self, id, text):
        """Вставить текст"""
        page = self.book.book.get(id)
        page["TextWidget"].insert(INSERT, text)
        page["Saved"] = False
        page["TextWidget"].update()

    def __close__(self, id):
        """Закрыть страницу"""
        if not self.book.book.get(id)["Saved"]:
            if askyesno(title="Сохранить?", message="Файл не сохранён. Сохранить?"):
                self.__save_as__(id)
        if len(self.book.book.pages) == 1:
            self.book.new()
        self.book.book.delete(id)

    def __save__(self, id):
        """Сохранить страницу"""
        if list(self.book.book.get(id)["Name"]).count("/") != 0:
            page = self.book.book.get(id)
            text = list(page["TextWidget"].text.get("1.0", END))
            del text[-1]
            text = "".join(text)
            with open(page["Name"], mode="w") as file:
                file.write(text)
            page["Saved"] = True
        else:
            self.__save_as__(id)

    def __save_as__(self, id):
        """Сохранить как"""
        name = asksaveasfilename(filetypes=self.app.settings["Global"]["FileTypes"],
                                 initialdir=self.app.settings["Global"]["HomeDir"],
                                 initialfile=self.book.book.get(id)["Name"])
        if name:
            self.__rename__(id, name=name)
            self.__save__(id)
        else:
            showwarning(message="Файл не сохранён.")
            
    class RenameDialog(DialogWindow):
        """Диалог переименования страницы"""
        def __init__(self, book):
            super().__init__(self)
            self.resizable(False, False)
            self.title("Переименовать")
            self.geometry("300x94")
            self.book = book
            self.entry = Entry(self, relief=SOLID, highlightthickness=0)
            self.entry.place(x=1, y=32, relw=1, w=-2, h=30)

            Frame(self, relief=SOLID, bd=1).place(x=1, y=1, relw=1, w=-2, h=30)
            Label(self, text="Введите новое имя:", relief=RAISED).place(x=2, y=2, relw=1, w=-4, h=28)
            Frame(self, relief=SOLID, bd=1).place(x=1, y=63, relw=1, w=-2, h=30)
            Button(self, text="Готово", command=self.check,
                   highlightthickness=0, relief=RAISED).place(x=2, y=64, relw=1, h=28, w=-4)

        def check(self):
            text = self.entry.get()
            print(text)
            if text != "":
                self.destroy()
                self.book.rename(id, text)

    def __rename__(self, id, name=None):
        """Переименовать страницу"""
        if not name:
            self.RenameDialog(self.book)
        else:
            self.book.rename(id, name)
        self.book.book.get(id)["Saved"] = False

    def __init__(self, root, id):
        """Инициализация"""
        super().__init__(root)
        self.id = id
        self.app = root.app
        self.title("OfficeRu Текстовый редактор")
        self.minsize(400, 600)
        self.protocol("WM_DELETE_WINDOW", partial(self.app.wm.close, self.id))

        """Тетрадь и управляющий"""
        self.book = CopybookWidget(self)
        self.book.place(x=1, y=1, relw=1, relh=1, w=-2, h=-2)

        self.new = self.book.new
        self.save = lambda: self.__save__(self.book.book.now)
        self.save_as = lambda: self.__save_as__(self.book.book.now)
        self.close = lambda: self.__close__(self.book.book.now)

        """Меню окна"""
        self.menu = Menu(self, tearoff=0)

        """Меню [Файл]"""
        self.menu.file = Menu(self.menu, tearoff=0)
        self.menu.file.add_command(label="Новое окно", command=self.app.am.text_editor)
        self.menu.file.add_command(label="Новый файл", command=self.new)
        self.menu.file.add_separator()
        self.menu.file.add_command(label="Открыть файл", command=self.open)
        self.menu.file.add_command(label="Открыть веб-страницу", command=self.open_web_page)
        self.menu.file.add_cascade(label="Недавние файлы")
        self.menu.file.add_separator()
        self.menu.file.add_command(label="Сохранить", command=self.save)
        self.menu.file.add_command(label="Сохранить как", command=self.save_as)
        self.menu.file.add_command(label="Сохранить всё", command=self.save_all)
        self.menu.file.add_separator()
        self.menu.file.add_command(label="Закрыть окно",
                                   command=partial(self.app.wm.close, self.id))
        self.menu.add_cascade(label="Файл", menu=self.menu.file)

        """Меню [Файл > Шаблоны]"""
        self.menu.file.patt = Menu(self.menu.file, tearoff=0)
        self.menu.file.patt.add_separator()
        self.menu.file.patt.add_command(label="Другие шаблоны")
        self.menu.file.insert_cascade(2, label="По шаблону", menu=self.menu.file.patt)

        """Меню [Файл > Запустить]"""
        self.menu.file.am = Menu(self.menu.file, tearoff=0)
        self.menu.file.am.add_command(label="Калькулятор", command=self.app.am.calculator)
        self.menu.file.insert_cascade(12, label="Запустить", menu=self.menu.file.am)

        """Меню [Правка]"""
        self.menu.edit = Menu(self.menu, tearoff=0)
        self.menu.edit.add_command(label="Поиск")
        self.menu.edit.add_command(label="Заменить")
        self.menu.edit.add_command(label="Форматирование")
        self.menu.add_cascade(label="Правка", menu=self.menu.edit)

        """Меню [Правка > Вставить]"""
        self.menu.edit.insert = Menu(self.menu.edit, tearoff=0)
        self.menu.edit.insert.add_command(label="Время", command=self.insert_time)
        self.menu.edit.insert.add_command(label="Дата", command=self.insert_date)
        self.menu.edit.insert.add_command(label="Цвет", command=self.insert_color)
        self.menu.edit.add_cascade(label="Вставить", menu=self.menu.edit.insert)

        """Меню [Инструменты]"""
        self.menu.edit.instrument = Menu(self.menu.edit, tearoff=0)
        self.menu.edit.add_cascade(label="Инструмент", menu=self.menu.edit.instrument)

        """Меню [Вид]"""
        self.menu.view = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Вид", menu=self.menu.view)

        """Меню [Настройки]"""
        self.menu.sett = Menu(self.menu, tearoff=0)
        self.menu.sett.add_command(label="Типы файлов", command=partial(FileTypesWindow, self))
        self.menu.sett.add_command(label="Шаблоны")
        self.menu.add_cascade(label="Настройки", menu=self.menu.sett)

        self.menu.add_command(label="Помощь")
        self.configure(menu=self.menu)
        self.book.new()
