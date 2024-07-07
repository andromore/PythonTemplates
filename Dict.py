"""Словарь"""


class Dict(object):
    """Словарь с возможностью блокировки добавления и удаления элементов"""
    
    def __init__(self, *args: str, __deleting: bool = True, __adding: bool = True, __raise: bool = True, __const: bool = False, **kwargs):
        """Инициализация"""
        super().__init__()
        super().__setattr__("__deleting", __deleting) # Можно ли удалять
        super().__setattr__("__adding", __adding) # Моно ли добавлять
        super().__setattr__("__const", __const) # Можно ли изменять
        super().__setattr__("__raise", __raise) # Генерировать ли ошибки
        for i in args:
            super().__setattr__(i, None)
        for i in kwargs.keys():
            super().__setattr__(i, kwargs[i])
            
    """Проверки"""
    
    def __exception__(self, exception: Exception = Exception, problem: str = "Exception", result: bool = ...):
        """Вызов ошибки"""
        if super().__getattribute__("__raise"): # Проверяем надо ли вызывать ошибку
            raise exception(problem) # Надо
        if result != ...:
            return result # Не надо
    
    def __validity__(self, key):
        """Проверка валидности ключа"""
        if type(key) != str or key[0:2] == "__": # Проверка валидности
            return super().__getattribute__("__exception__")(KeyError, "Key name is illegal", False) # Если не валидный
        return True # Ключ валидный
    
    def __keys__(self, key: str):
        """Проверка наличия соответствующего ключа"""
        if super().__getattribute__("__validity__")(key): # Если ключ валидный - проверяем наличие
            for i in super().__getattribute__("__dict__").keys(): # Ищем ключ
                if i == key: # Проверяем - тот ли ключ
                    return True # Найден валидный люч
        return False # Ключ валидный, не найден и ошибку вызывать не надо
    
    """Dict[key]"""
    
    def __getitem__(self, key: str):
        """>>> Dict[key]"""
        if super().__getattribute__("__keys__")(key): # Если есть такой ключ
            return super().__getattribute__(key) # Возвращаем
        return super().__getattribute__("__exception__")(KeyError, "There is no such key", None) # Если нет ключа и не была вызвана ошибка
    
    def __setitem__(self, key: str, value):
        """>>> Dict[key] = value"""
        if not super().__getattribute__("__keys__")(key): # Такого нет, значит можно добавить
            if super().__getattribute__("__adding"): # Можно добавить
                super().__setattr__(key, value) # Добавляем
                return # Завершаемся
            return super().__getattribute__("__exception__")(TypeError, "Object is constant", ...) # Надо ли вызывать ошибку
        if super().__getattribute__("__const"): # Если объект константный
            return super().__getattribute__("__exception__")(TypeError, "Object is constant", ...) # Надо ли вызывать ошибку
        super().__setattr__(key, value) # Меняем
        
    def __delitem__(self, key: str):
        """>>> del Dict[key]"""
        if not super().__getattribute__("__deleting"): # Если удалять нельзя - ошибка
            return super().__getattribute__("__exception__")(KeyError, "Deleting is illegal for this object", ...) # Надо ли вызывать ошибку
        if not super().__getattribute__("__keys__")(key): # Убить мертвеца
            return super().__getattribute__("__exception__")(KeyError, "Key does not exists", ...) # Надо ли вызывать ошибку
        super().__delattr__(key) # Удаляем
    
    """Dict.property"""
    
    def __getattribute__(self, name: str):
        """>>> Dict.name"""
        return self[name]
    
    def __setattr__(self, name: str, value):
        """>>> Dict.name = value"""
        self[name] = value
        
    def __delattr__(self, name: str):
        """>>> del Dict.name"""
        del self[name]
        
    """Преобразования типов и представления"""
    
    def __used__(self):
        """Список всех ключей"""
        result = []
        for i in super().__getattribute__("__dict__").keys():
            if i[0:2] != "__":
                result.append(i)
        return result
    
    def __len__(self):
        """Количество записей"""
        return len(super().__getattribute__("__used__")())
    
    def __contains__(self, key: str) -> bool:
        """Проверка наличия ключа >>> key in Dict"""
        return super().__getattribute__("__keys__")(key)
    
    def __iter__(self):
        """Список пар [ключ, значение] >>> list(Dict)"""
        result = []
        for i in super().__getattribute__("__used__")():
            result.append([i, self[i]])
        return iter(result)
    
    def __str__(self):
        """Строка >>> str(Dict)"""
        string = ""
        for i in super().__getattribute__("__used__")():
            string += ", " + i + ": " + str(super().__getattribute__(i))
        return f"{{{string[2:]}}}"
