"""Кодирование и шифрование"""


FROM = 'from'
TO = 'to'

SYMBOL = 'symbol'
BYTE = 'byte'

TEXTtoTEXT = "text-text"
FILEtoFILE = "file-file"
TEXTtoFILE = "text-file"
FILEtoTEXT = "file-text"

ENCODE = 'encode'
DECODE = 'decode'


class EncodingTable:
    """Кодировочная таблица"""

    @classmethod
    def json(cls, file, mode=FROM, key=SYMBOL):
        """Чтение и запись из файла Json"""
        if mode == FROM:
            # TODO
            ...
        elif mode == TO:
            # TODO
            ...
        else:
            raise Exception("mode: ['from', 'to']")

    @classmethod
    def csv(cls, file, mode=FROM):
        """Чтение и запись из файла Csv"""
        if mode == FROM:
            ...
        elif mode == TO:
            ...
        else:
            raise Exception("mode: ['from', 'to']")

    @classmethod
    def new(cls, n=1):
        """Новая таблица n байт на символ"""
        assert type(n) == int and n > 0, "n - количество байт на символ (целое положительное число)"
        table = []
        for i in range(0, 256 ** n):
            table.append([i, ""])
        return cls(table=table)

    def __init__(self, table=None):
        """Инициализация"""
        assert type(table) == list
        self.table = table if table else []

    def get(self, input, mode=SYMBOL):
        """Получить значение"""
        if mode == SYMBOL:
            assert type(input) == str, "input: str"
            for i in self.table:
                if i[1] == input:
                    return i[0]
            print("-", input, "-", sep="")
            raise Exception("input not in EncodingTable")
        elif mode == BYTE:
            assert type(input) == int, "input: byte"
            assert -1 < input < len(self.table), "input not in EncodingTable"
            return self.table[input][1]
        else:
            raise Exception("type: ['symbol', 'byte']")

    def set(self, key, value, mode=SYMBOL):
        """Установить значение"""
        if mode == SYMBOL:
            self.set(value, key, mode=BYTE)
        elif mode == BYTE:
            assert type(key) == int and type(value) == str, "key: byte, value: symbol"
            assert -1 < key < len(self.table), "key not in EncodingTable"
            self.table[key] = [key, value]
        else:
            raise Exception("type: ['symbol', 'byte']")

    def range(self, alfabet, start=0):
        """Составить таблицу из алфавита"""
        assert start + len(alfabet) < len(self.table), "Алфавит не уместится в таблице"
        assert type(alfabet) == str, "alfabet: str"
        k = start
        for i in alfabet:
            self.set(k, i, mode=BYTE)
            k += 1

    def mix(self):
        """Перемешать таблицу"""
        ...

    def __bool__(self):
        return bool(self.table)

    def __getitem__(self, item):
        if type(item) == int:
            return self.get(item, mode=BYTE)
        elif type(item) == str:
            return self.get(item, mode=SYMBOL)
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if type(key) == int and type(value) == str:
            self.set(key, value, mode=BYTE)
        elif type(key) == str and type(value) == int:
            self.set(key, value, mode=SYMBOL)
        else:
            raise (KeyError, ValueError)

    def __delitem__(self, item):
        if type(item) == int:
            self.set(item, "", mode=BYTE)
        elif type(item) == str:
            self.set(self.get(item, mode=SYMBOL), "", mode=BYTE)
        else:
            raise KeyError

    def __iter__(self):
        return iter(self.table)

    def __contains__(self, value):
        if type(value) == int:
            for i in self.table:
                if value == i[0]:
                    return True
            return False
        elif type(value) == str:
            for i in self.table:
                if value == i[1]:
                    return True
            return False
        else:
            raise ValueError


class Encoder:
    """Кодировщик"""

    def __init__(self, table):
        """Инициализация"""
        self.table = table

    def code(self, input: str, output: str = None, mode=TEXTtoTEXT, code=ENCODE):
        """Кодировать
        \ninput - кодируемые текст или имя файла
        \noutput - имя файла при result = file
        \nmode - формат преобразования
        \ncode - закодировать или раскодировать"""
        assert mode in (FILEtoTEXT, TEXTtoFILE, FILEtoFILE, TEXTtoTEXT), \
            "mode: ['file-file', 'file-text', 'text-file', 'text-text']"
        m1, m2 = mode.split("-")

        if m1 == "text":
            assert type(input) == str or type(input) == bytes, "text-text or text-file require a string in 'input'"
            data = input
        elif m1 == "file":
            assert type(input) == str or type(input) == bytes, "file-text or file-file require a file name in 'input'"
            with open(input, mode='rb') as file:
                data = file.read()
        else:
            raise Exception("mode: ['text', 'file']")

        data = list(data)

        if code == ENCODE:
            """Закодировать"""
            for i in range(len(data)):
                data[i] = self.table.get(data[i], mode=SYMBOL)
            data = bytes(data)
        elif code == DECODE:
            """Раскодировать"""
            for i in range(len(data)):
                data[i] = self.table.get(data[i], mode=BYTE)
            data = "".join(data)
        else:
            raise Exception("code: ['encode', 'decode']")

        if m2 == "text":
            if output is not None:
                print("text-text or file-text do not use 'output' parameter")
            return data
        elif m2 == "file":
            assert output is not None, "file-file or text-file require a file name in 'output'"
            if code == ENCODE:
                with open(output, mode='wb') as file:
                    file.write(data)
            elif code == DECODE:
                with open(output, mode='w') as file:
                    file.write(data)
            else:
                raise Exception("code: ['encode', 'decode']")
        else:
            raise Exception("result: ['text', 'file']")


class Encrypter:
    """Шифровальщик"""
    # TODO


a = EncodingTable.new(n=1)
a.range("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890 \n!?,.")
b = Encoder(a)
b.code("???Hello, world!!!", mode=TEXTtoFILE, output="./1.txt")
