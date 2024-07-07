"""Различные классы и функции"""

def passing(*a, **b):
    """Ничего не делает"""
    pass

def partial(function, *a, **b):
    """Возвращает функцию с подставленными параметрами"""

    def func(*c, **d):
        return function(*a, *c, **b, **d)

    return func
