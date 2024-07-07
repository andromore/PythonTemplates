"""Вспомогательные функции для работы со строками"""

DIGITS = "0123456789"

def is_integer(string: str) -> bool:
    """Является ли строка целым числом"""
    if type(string) != str:
        raise ValueError("Неверный тип аргумента: " + str(type(string)))
    result = True
    for i in string:
        result = result and (i in DIGITS)
    return result

def is_float(string: str) -> bool:
    """Является ли строка числом с плавающей точкой"""
    if type(string) != str:
        raise ValueError("Неверный тип аргумента: " + str(type(string)))
    return (string.count(".") == 1) and (string[0] != ".") and (string[-1] != ".") and is_integer(string.replace(".", ""))

def is_real(string: str) -> bool:
    """Является ли строка вещественным числом"""
    if type(string) != str:
        raise ValueError("Неверный тип аргумента: " + str(type(string)))
    return is_float(string) or is_integer(string)

def is_Date(text: str, separator: str = ".") -> bool:
    """Является ли строка датой"""
    if not type(text) == str:
        raise ValueError("Неверный тип аргумента: " + str(type(text)))
    if text.count(separator) == 2:
        splitted = text.split(separator)
        if is_integer(splitted[0]) and is_integer(splitted[1]) and is_integer(splitted[2]):
            return True
    return False

def is_Time(text: str, separator: str = ":") -> bool:
    """Является ли строка датой"""
    if not type(text) == str:
        raise ValueError("Неверный тип аргумента: " + str(type(text)))
    if text.count(separator) == 2:
        splitted = text.split(separator)
        if is_integer(splitted[0]) and is_integer(splitted[1]) and is_integer(splitted[2]):
            return True
    return False

class String:
    """Строка с возможностью менять символы"""

    def __init__(self, arg):
        """Инициализация одним аргументом"""
        self.__string = str(arg)