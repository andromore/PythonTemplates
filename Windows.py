"""Окна и оконный менеджер"""

from tkinter import Tk, Toplevel

class Window(Toplevel):
    """Окно"""

    show = Toplevel.deiconify
    hide = Toplevel.withdraw

class DialogWindow(Window):
    """Диалоговое окно"""

    def __init__(self, master, **args):
        """Инициализация"""
        super().__init__(master, **args)
        self.attributes("-topmost", True)
        self.attributes("-type", "dialog")
        self.focus_set()
        self.grab_set()
        self.lift()

class Root(Tk):
    """Приложение tkinter"""

    def __init__(self, app):
        """Инициализация"""
        super().__init__()
        self.app = app

    def show(self):
        """Показать окно"""
        self.deiconify()

    def hide(self):
        """Скрыть окно"""
        self.withdraw()

class WindowsManager:
    """Менеджер окон"""

    def __init__(self, application):
        """Инициализация"""
        self.key = 0
        self.windows = dict()
        self.app = application
        self.root = self.app.root

    def new(self, app):
        """Создать новое окно"""
        self.windows[self.key] = app(self.root, self.key)
        self.key += 1
    
    def close(self, id):
        """Закрыть окно"""
        if not id in self.windows.keys():
            raise KeyError("Ошибка закрытия окна: такого окна нет")
        self.windows[id].destroy()
        del self.windows[id]
        if len(self.windows) == 0:
            self.root.quit()
