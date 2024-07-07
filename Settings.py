"""Настройки"""

# Различные настройки

from Dict import Dict

# Менеджер настроек

class SettingsManager:
    """Менеджер настроек"""

    @staticmethod
    def __dict(settings):
        result = dict()
        for i in dir(settings):
            result[i] = settings[i]
        return result

    def __init__(self, launcher):
        """Инициализация"""
        self.launcher = launcher

    def load(self):
        """Загрузить настройки"""

    def save(self):
        """Сохранить настройки"""

    def create(self):
        """Создать настройки"""
        return Dict(Global=Dict(FileTypes=[["All files", "*.*"],
                                           ["Plain text", "*.txt"],
                                           ["Python script", "*.py"],
                                           ["C++ source code", "*.cpp"],
                                           ["C source code", "*.c"],
                                           ["C++ header file", "*.hpp"],
                                           ["C header file", "*.h"]],
                                HomeDir="/home/andromore"))

    def check(self):
        """Проверить настройки"""

    def find(self):
        """Найти файл настроек"""
