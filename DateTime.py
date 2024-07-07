"""Дата и время"""

from Strings import is_Date, is_Time

from time import sleep
from datetime import datetime

class Date:
    """Класс для удобной работы с датами"""    

    separator = "."

    def __init__(self, arg: list | tuple | str, *args) -> None:
        """Инициализация кортежем, строкой, одним целым числом или тремя целыми числами"""
        if type(arg) == str and len(args) == 0: # Инициализация строкой
            if not self.is_Date(arg, separator=self.separator):
                raise ValueError("Строка не является датой")
            arg = list(arg.split(self.separator))
            for i in range(len(arg)):
                arg[i] = int(arg[i])
            self.day, self.month, self.year = arg
        elif type(arg) == int and len(args) == 2: # Инициализация днями, месяцами и годами
            self.day, self.month, self.year = arg, *args
        elif (type(arg) == list or type(arg) == tuple) and len(args) == 0: # Инициализация списком или кортежем
            self.day, self.month, self.year = arg
        elif type(arg) == int and len(args) == 0: # Инициализация днями
            self.day = arg
            self.month, self.year = 0, 0
        else:
            raise ValueError("Непонятны аргументы")
        self.__checking()  

    @classmethod
    def is_Date(cls, string: str) -> bool:
        return is_Date(string, cls.separator)

    @classmethod
    def now(cls):
        """Возвращает объект класса с текущей датой"""        
        a = str(datetime.now())
        return cls((int(a[8] + a[9]), int(a[5] + a[6]), int(a[0] + a[1] + a[2] + a[3])))

    def update(self) -> None:
        """Обновляет дату экземпляра класса"""
        a = str(datetime.now())
        self.day = int(a[8] + a[9])
        self.month = int(a[5] + a[6])
        self.year = int(a[0] + a[1] + a[2] + a[3])
        self.__checking()

    def __str__(self) -> str:
        self.__checking()
        if self.day <= 9:
            day = "0" + str(self.day)
        else:
            day = str(self.day)
        if self.month <= 9:
            month = "0" + str(self.month)
        else:
            month = str(self.month)
        return day + Date.separator + month + Date.separator + str(self.year)

    def __checking(self):
        """Функция внутреннего использования"""  
        if type(self.day) != int or type(self.month) != int or type(self.year) != int:
            raise Exception("Ошибка: хранимые данные о дне, месяце и годе должны быть типа int")      
        while not((1 <= self.month <= 12) and ((1 <= self.day <= 31) if self.month in [1, 3, 5, 7, 8, 10, 12] else (1 <= self.day <= 30) if self.month in [4, 6, 9, 11] else ((1 <= self.day <= 28) if self.year % 4 != 0 else (1 <= self.day <= 29)))):
            if self.month >= 13:
                self.year += 1
                self.month -= 12
            elif self.month <= 0:
                self.year -= 1
                self.month += 12
            if self.month in [1, 3, 5, 7, 8, 10, 12]:
                if self.day >= 32:
                    self.day -= 31
                    self.month += 1
            elif self.month in [4, 6, 9, 11]:
                if self.day >= 31:
                    self.day -= 30
                    self.month += 1
            elif self.month == 2:
                if self.year % 4 == 0:
                    if self.day >= 30:
                        self.day -= 29
                        self.month += 1
                else:
                    if self.day >= 29:
                        self.day -= 28
                        self.month += 1
            if self.day <= 0:
                self.month -= 1
                if self.month in [1, 3, 5, 7, 8, 10, 12]:
                    self.day += 31
                elif self.month in [4, 6, 9, 11]:
                    self.day += 30
                elif self.month == 2:
                    if self.year % 4 == 0:
                        self.day += 29
                    else:
                        self.day += 28
        return self

    def __add__(self, other):
        if type(other) != Date:
            other = Date(other)
        return Date(self.day + other.day, self.month + other.month, self.year + other.year).__checking()

    def __sub__(self, other):
        if type(other) != Date:
            other = Date(other)
        return Date(self.day - other.day, self.month - other.month, self.year - other.year).__checking()

    def __lt__(self, other):
        self.__checking()
        if type(other) != Date:
            other = Date(other)
        if self.year > other.year:
            return True
        elif self.year < other.year:
            return False
        else:
            if self.month > other.month:
                return True
            elif self.month < other.month:
                return False
            else:
                if self.day > other.day:
                    return True
                else:
                    return False

    def __gt__(self, other):
        self.__checking()
        if type(other) != Date:
            other = Date(other)
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        else:
            if self.month < other.month:
                return True
            elif self.month > other.month:
                return False
            else:
                if self.day < other.day:
                    return True
                else:
                    return False

    def __eq__(self, other):
        self.__checking()
        if type(other) != Date:
            other = Date(other)
        if self.year == other.year and self.month == other.month and self.day == other.day:
            return True
        else:
            return False

    def __ne__(self, other):
        self.__checking()
        if type(other) != Date:
            other = Date(other)
        if self.year == other.year and self.month == other.month and self.day == other.day:
            return False
        else:
            return True

    def __le__(self, other):
        self.__checking()
        if type(other) != Date:
            other = Date(other)
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        else:
            if self.month < other.month:
                return True
            elif self.month > other.month:
                return False
            else:
                if self.day <= other.day:
                    return True
                elif self.day > other.day:
                    return False

    def __ge__(self, other):
        self.__checking()
        if type(other) != Date:
            other = Date(other)
        if self.year < other.year:
            return False
        elif self.year > other.year:
            return True
        else:
            if self.month < other.month:
                return False
            elif self.month > other.month:
                return True
            else:
                if self.day < other.day:
                    return False
                elif self.day >= other.day:
                    return True

class Time:
    """Класс для удобной работы с временем"""   

    separator = ":"

    def __init__(self, arg: list | tuple | str, *args) -> None:
        """Инициализация кортежем, строкой, одним целым числом или тремя целыми числами"""
        if type(arg) == str and len(args) == 0: # Инициализация строкой
            if not self.is_Date(arg, separator=self.separator):
                raise ValueError("Строка не является временем")
            arg = list(arg.split(self.separator))
            for i in range(len(arg)):
                arg[i] = int(arg[i])
            self.hour, self.minute, self.seconds = arg
        elif type(arg) == int and len(args) == 2: # Инициализация днями, месяцами и годами
            self.hour, self.minute, self.seconds = arg, *args
        elif (type(arg) == list or type(arg) == tuple) and len(args) == 0: # Инициализация списком или кортежем
            self.hour, self.minute, self.seconds = arg
        elif type(arg) == int and len(args) == 0: # Инициализация днями
            self.hour = arg
            self.minute, self.seconds = 0, 0
        else:
            raise ValueError("Непонятны аргументы")
        self.__checking()

    @classmethod
    def is_Time(cls, text: str) -> bool:
        return is_Time(text)

    def update(self) -> None:
        """Обновляет время экземпляра класса"""
        a = str(datetime.now())[11:19]
        self.hour = int(a[0] + a[1])
        self.minute = int(a[3] + a[4])
        self.second = int(a[6:])

    @classmethod
    def now(cls):
        """Возвращает объект класса с текущим временем"""
        a = str(datetime.now())[11:19]
        return cls((int(a[0] + a[1]), int(a[3] + a[4]), int(a[6:])))

    def __str__(self) -> str:
        if self.second <= 9:
            second = "0" + str(self.second)
        else:
            second = self.second
        if self.minute <= 9:
            minute = "0" + str(self.minute)
        else:
            minute = self.minute
        if self.hour <= 9:
            hour = "0" + str(self.hour)
        else:
            hour = self.hour
        return str(hour) + Time.separator + str(minute) + Time.separator + str(second)

    def __checking(self):
        """Проверка диапазонов после арифметических действий"""
        if not(0 <= self.second < 60):
            tmp = self.second
            self.second = tmp % 60
            self.minute += tmp // 60
        if not(0 <= self.minute < 60):
            tmp = self.minute
            self.minute = tmp % 60
            self.hour += tmp // 60
        if not(0 <= self.second < 24):
            self.hour %= 24
        return self

    def __add__(self, other):
        if type(other) != Time:
            other = Time(other)
        return Time(self.hour + other.hour, self.minute + other.minute, self.second + other.second).__checking()

    def __sub__(self, other):
        if type(other) != Time:
            other = Time(other)
        return Time(self.hour - other.hour, self.minute - other.minute, self.second - other.second).__checking()

    def __eq__(self, other):
        self.__checking()
        if type(other) != Time:
            other = Time(other)
        if self.hour == other.hour and self.minute == other.minute and self.second == other.second:
            return True
        else:
            return False

    def __ne__(self, other):
        self.__checking()
        if type(other) != Time:
            other = Time(other)
        if self.hour == other.hour and self.minute == other.minute and self.second == other.second:
            return False
        else:
            return True

    def __lt__(self, other):
        self.__checking()
        if type(other) != Time:
            other = Time(other)
        if self.hour > other.hour:
            return True
        elif self.hour < other.hour:
            return False
        else:
            if self.minute > other.minute:
                return True
            elif self.minute < other.minute:
                return False
            else:
                if self.second > other.second:
                    return True
                else:
                    return False

    def __gt__(self, other):
        self.__checking()
        if type(other) != Time:
            other = Time(other)
        if self.hour < other.hour:
            return True
        elif self.hour > other.hour:
            return False
        else:
            if self.minute < other.minute:
                return True
            elif self.minute > other.minute:
                return False
            else:
                if self.second < other.second:
                    return True
                else:
                    return False

    def __le__(self, other):
        self.__checking()
        if type(other) != Time:
            other = Time(other)
        if self.hour < other.hour:
            return True
        elif self.hour > other.hour:
            return False
        else:
            if self.minute < other.minute:
                return True
            elif self.minute > other.minute:
                return False
            else:
                if self.second <= other.second:
                    return True
                elif self.second > other.second:
                    return False

    def __ge__(self, other):
        self.__checking()
        if type(other) != Time:
            other = Time(other)
        if self.hour < other.hour:
            return False
        elif self.hour > other.hour:
            return True
        else:
            if self.minute < other.minute:
                return False
            elif self.minute > other.minute:
                return True
            else:
                if self.second < other.second:
                    return False
                elif self.second >= other.second:
                    return True
