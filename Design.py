"""Обработка изображений, цвет"""
from PIL import Image as Img, ImageDraw as ImgDraw
from os import getcwd
from random import randint
from requests import get


class Color:
    """Класс для работы с цветами"""

    """Цвета"""
    Black = "#000000"
    White = "#FFFFFF"
    Yellow = "#FFFF00"
    Red = "#FF0000"
    Green = "#00FF00"
    Blue = "#0000FF"
    SysGray = "#D9D9D9"
    Purple = "#8B00FF"
    Pink = "#FFC0CB"
    Magenta = "#FF00FF"
    SeaWave = "#00FFFF"
    Orange = "#FFA500"
    Gray = "#808080"

    @staticmethod
    def FormatColor(color, to: type = str):
        """Преобразование формата цвета"""
        if type(color) == str:
            if to == str:
                return color
            elif to == list:
                return [int("0x" + color[1:3], 16), int("0x" + color[3:5], 16), int("0x" + color[5:7], 16)]
        elif type(color) == list:
            if to == list:
                return color
            elif to == str:
                return "#" + hex(color[0])[2:] + hex(color[1])[2:] + hex(color[2])[2:]
        raise ValueError("type(color) -> ???")

    @staticmethod
    def ColorSum(color1, color2, k=0.5, to: type = str):
        """Смешивание цветов"""
        color1 = Color.FormatColor(color1, to=list)
        color2 = Color.FormatColor(color2, to=list)
        func = lambda n: round(color1[n] * (1 - k) + color2[n] * k)
        return Color.FormatColor([func(0), func(1), func(2)], to=to)


class Image:
    """Инструмент работы с изображениями"""

    @staticmethod
    def get(url: str):
        """Открыть изображение по url"""
        return Image(url, Img.open(get(url, stream=True).raw))

    @staticmethod
    def open(openfile: str):
        """Открыть файл изображения"""
        return Image(openfile, Img.open(openfile))

    @staticmethod
    def new(mode: str = 'RGB', size: tuple = (256, 256)):
        """Создать новое изображение"""
        return Image(getcwd() + "/new.png", Img.new(mode=mode, size=size))

    def __init__(self, file, image):
        """Инициализация"""
        self.file = file
        self.image = image
        self.tool = ImgDraw.Draw(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.size = self.image.size

        self.show = self.image.show
        self.load = self.image.load
        self.point = self.tool.point

    def save(self, savefile: str = None, format: str = "PNG"):
        """Сохранить изображение"""
        if savefile:
            self.image.save(savefile, format)
        else:
            self.image.save(self.file, format)

    def copy(self):
        """Копировать изображение"""
        return self

    def part(self, coordinates: tuple):
        """Получить часть изображения"""
        image = self
        image.image = self.image.crop(coordinates)
        return image

    def resize(self, size: tuple) -> None:
        """Изменить размер изображение"""
        image = self
        image.image.thumbnail(size)
        return image

    def rotate(self, degrees: int):
        """Повернуть изображение на указанное количество градусов"""
        image = self
        image.image = self.image.rotate(degrees)
        return image

    def apply(self, other, k=0.5):
        """Наложить два изображения"""
        return Img.blend(self.image, other.image, k)


class Filter:
    @staticmethod
    def join(image, *filters, x1=None, y1=None, x2=None, y2=None):
        """Объединить фильтры"""
        load = image.load()
        w = range(x1, x2 + 1) if x1 and x2 else range(image.width)
        h = range(y1, y2 + 1) if y1 and y2 else range(image.height)
        for x in w:
            for y in h:
                rgb = list(load[x, y])
                for i in filters:
                    rgb = i(rgb)
                image.point((x, y), tuple(rgb))
        return image

    @staticmethod
    def negative(rgb, R=True, G=True, B=True):
        """Фильтр негатив"""
        rgb[0] = (255 - rgb[0]) if R else rgb[0]
        rgb[1] = (255 - rgb[1]) if G else rgb[1]
        rgb[2] = (255 - rgb[2]) if B else rgb[2]
        return rgb

    @staticmethod
    def averaging(rgb, R=True, G=True, B=True):
        """Усреднение изображения - чёрно-белый фильтр/оттенки серого"""
        s = (rgb[0] + rgb[1] + rgb[2]) // 3
        return [s if R else rgb[0], s if G else rgb[1], s if B else rgb[2]]

    @staticmethod
    def sepia(rgb, R=1, G=1, B=1, k=20):
        """Сепия"""
        s = (rgb[0] + rgb[1] + rgb[2]) // 3
        return [s + k * R, s + k * G, s + k * B]

    @staticmethod
    def interference(rgb, R=True, G=True, B=True, k=50):
        """Шумы"""
        r = rgb[0] + (randint(-k, k) if R else 0)
        g = rgb[1] + (randint(-k, k) if G else 0)
        b = rgb[2] + (randint(-k, k) if B else 0)
        return [r, g, b]

    @staticmethod
    def round(rgb, R=True, G=True, B=True, k=16):
        """Округление цвета"""
        r = round(rgb[0] / k) * k
        g = round(rgb[1] / k) * k
        b = round(rgb[2] / k) * k
        return [r if R else rgb[0], g if G else rgb[1], b if B else rgb[2]]
