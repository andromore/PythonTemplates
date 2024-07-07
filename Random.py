"""Случайности"""
from Tools import partial

import random

class Random:
    """Класс для работы со случайными значениями"""

    init = partial(random.seed, version=2)
    
    @staticmethod
    def integer(start, stop):
        """Возвращает псевдослучайное целое число в диапазоне от "a" до "b" """
        assert isinstance(start, (int, float)) and isinstance(stop, (int, float))
        return random.randint(start, stop)
    
    @staticmethod
    def figure():
        """Возвращает цифру от 0 до 9 """
        return Random.integer(0, 9)
    
    @staticmethod
    def boolean():
        """Возвращает логическое значение True или False"""
        return bool(Random.integer(0, 1))

    @staticmethod
    def range(start, stop, step):
        """Возвращает псевдослучайное целое число в диапазоне от "start" до "stop" с шагом "step" """
        assert isinstance(start, (int, float)) and isinstance(stop, (int, float)) and isinstance(step, (int, float))
        return random.randrange(start, stop, step)

    @staticmethod
    def fraction():
        """Возвращает псевдослучайное вещественное число от 0 до 1"""
        return random.random()

    @staticmethod
    def floating(start, stop):
        """Возвращает псевдослучайное вещественное число от числа "a" до числа "b" """
        assert isinstance(start, (int, float)) and isinstance(stop, (int, float))
        return random.uniform(start, stop)

    @staticmethod
    def randin(a):
        """Возвращает псевдослучайный элемент из набора значений"""
        assert isinstance(a, (str, list, tuple, dict, set, frozenset))
        if isinstance(a, str) or isinstance(a, list) or isinstance(a, tuple):
            b = Random.integer(0, len(a) - 1)
            return a[b]
        elif isinstance(a, dict):
            b = list(a.keys())
            c = Random.integer(0, len(b) - 1)
            return a[b[c]]
        elif isinstance(a, set) or isinstance(a, frozenset):
            b = list(a)
            c = Random.integer(0, len(b) - 1)
            return b[c]
        raise

    @staticmethod
    def percent():
        """Возвращает псевдослучайное число от 0 до 100"""
        return Random.integer(0, 100)
