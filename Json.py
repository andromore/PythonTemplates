"""Json"""

from json import dump, load

def write(file: str, data, encoding: str = "utf-8") -> None:
    """Сохранить в Json"""
    with open(file, mode="w", encoding=encoding) as file:
        dump(data, file)

def read(file: str, encoding="utf-8"):
    """Загрузить из Json"""
    with open(file, mode="r", encoding=encoding) as file:
        data = load(file)
    return data
