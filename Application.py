"""Приложение и лаунчер"""

from Settings import SettingsManager
from Windows import WindowsManager, Root
from TextEditor import TextEditorApp
from Calculator import CalculatorApp
from Tools import partial

class AppsManager:
    """Менеджер приложений"""

    def __init__(self, application):
        """Инициализация"""
        self.app = application
        self.wm = self.app.wm

        self.text_editor = partial(self.wm.new, TextEditorApp)
        self.calculator = partial(self.wm.new, CalculatorApp)

class Application:
    """Приложение"""

    def __init__(self, launcher):
        """Инициализация"""
        self.launcher = launcher
        self.root = Root(self)
        self.root.hide()
        self.wm = WindowsManager(self)
        self.am = AppsManager(self)

    def run(self):
        """Запуск"""
        self.settings = self.launcher.settings
        self.am.text_editor()
        self.root.mainloop()

class Launcher:
    """Загрузчик приложения"""

    def __init__(self):
        """Инициализация"""
        self.sm = SettingsManager(self)
        self.app = Application(self)

        """Загрузка"""
        self.settings = self.sm.create()

        """Запуск"""
        self.app.run()

        """Завершение"""
        
