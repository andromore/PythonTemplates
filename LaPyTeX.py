"""Python library for generation LaTeX documents: main module"""

from DateTime import Date as __Date
from Dict import Dict as __Dict

"""Elements arguments"""

class Argument:
    """Basic class for element argument"""
    def __init__(self, *args, optional: bool = False, **kwargs):
        """LaTeX argument [*args, **kwargs] if optional or {*args, **kwargs} if required (not optional)"""
        self.args = list(args)
        self.kwargs = kwargs
        self.optional = optional

    def __str__(self) -> str:
        arg = self.args
        for i in self.kwargs.keys():
            arg.append(f"{i}={self.kwargs[i]}")
        return f"{'[' if self.optional else '{'}{', '.join(arg)}{']' if self.optional else '}'}"

class RequiredArgument:
    """Class for required element arguments"""
    def __init__(self, *args, **kwargs):
        """LaTeX required argument {*args, **kwargs}"""
        self.args = list(args)
        self.kwargs = kwargs

    def __str__(self) -> str:
        arg = self.args
        for i in self.kwargs.keys():
            arg.append(f"{i}={self.kwargs[i]}")
        return f"{{{', '.join(arg)}}}"

class OptionalArgument:
    """Class for optional element arguments"""
    def __init__(self, *args, **kwargs):
        """LaTeX optional argument [*args, **kwargs]"""
        self.args = list(args)
        self.kwargs = kwargs

    def __str__(self) -> str:
        arg = self.args
        for i in self.kwargs.keys():
            arg.append(f"{i}={self.kwargs[i]}")
        return f"[{', '.join(arg)}]"

def __check__arguments_list_types(*args) -> bool:
    """Check list of arguments for if they really are arguments"""
    result = True
    for i in args:
        result = result and (type(i) == Argument or type(i) == OptionalArgument or type(i) == RequiredArgument)
    return result

"""Basic blocks"""

class Element:
    """Basic class for all elements"""
    def __init__(self, name: str, *args, outline: bool = False):
        assert type(name) == str and __check__arguments_list_types(*args) and type(outline) == bool
        self.name = name
        self.args = list(args)
        self.outline = outline
        for _ in range(self.args.count(None)): self.args.remove(None)

    def __str__(self) -> str:
        return f"\\{self.name}{''.join(list(map(str, self.args)))}" + ('\n' if self.outline else '')
    
class Double:
    """Basic class for elements with beginning and ending parts"""
    def __init__(self, begin, end, inner = None, inline: bool = False):
        self.beginning = begin
        self.ending = end
        self.inner = inner
        self.inline = inline

    def __str__(self):
        begin = str(self.beginning) + ("\n" if not self.inline else "")
        end = str(self.ending) + ("\n" if not self.inline else "")
        return f"{begin}{str(self.inner) if self.inner else ''}{end}"

class Environment(Double):
    """Basic class for all environments"""
    def __init__(self, name: str, inner = None, *args, inline: bool = False):
        assert type(name) == str and type(inline) == bool and __check__arguments_list_types(*args)
        super().__init__(Element('begin', RequiredArgument(name), *args, outline = not inline), Element("end", RequiredArgument(name), outline = not inline), inner = inner)

"""Defining elements"""

"""Counters"""

"""Lengths"""

"""Math"""

class Math:
    class TexInline(Double):
        """$ ... $"""
        def __init__(self, inner): # Вариант inner = None не обсуждается, т.к. получаем строку $$, что будет являться ошибкой
            super().__init__("$", "$", inner = inner, inline = True)

    class TexOutline(Double):
        """$$ ... $$"""
        def __init__(self, inner): # Вариант inner = None по аналогии с TexInline и требует проверки
            super().__init__("$$", "$$", inner = inner)

    class Math(Environment):
        """\\begin{math} ... \\end{math}"""
        def __init__(self, inner = None):
            super().__init__("math", inner, inline = True)

    class DisplayMath(Environment):
        """\\begin{displaymath} ... \\end{displaymath}"""
        def __init__(self, inner = None):
            super().__init__("displaymath", inner)

    class Equation(Environment):
        """\\begin{equation} ... \\end{equation}"""
        def __init__(self, inner = None, dotted: bool = False):
            super().__init__("equation" + ("*" if dotted else ""), inner)

    class Gather(Environment):
        """\\begin{gather} ... \\end{gather}"""
        def __init__(self, inner = None, dotted: bool = False):
            super().__init__("gather" + ("*" if dotted else ""), inner)

"""Table blocks"""

"""Graphics blocks"""

"""Sectioning blocks"""

"""Different blocks"""

class Letter(Double):
    """Environment \\makeatletter \\makeatother"""
    def __init__(self, inner = None):
        super().__init__(Element("makeatletter", outline = True), Element("makeatother", outline = True), inner = inner)

"""Document and its parts"""

class DocumentClass(Element):
    """Class of LaTeX document"""
    def __init__(self, cls: str, arg: OptionalArgument = None):
        super().__init__("documentclass", arg, RequiredArgument(cls))

class Title(Element):
    """Title of LaTeX document"""
    def __init__(self, title: str):
        super().__init__("title", RequiredArgument(title))

class Authors(Element):
    """Authors of LaTeX document"""
    def __init__(self, author: str, *authors: str):
        super().__init__("author", RequiredArgument(author + (" \\and " if authors else "") + " \\and ".join(authors)))
    
class Date(Element):
    """Date creation of LaTeX document"""
    def __init__(self, date: str = None):
        super().__init__("date", RequiredArgument(date if date else str(__Date.now())))

class Document(Environment): # Дочерние элементы
    """Document environment"""
    def __init__(self):
        super().__init__("document", [])

    def add(self, element):
        self.inner.append(element)

    def __str__(self, end: str = "\n"):
        self.inner = end.join(self.inner) + end
        return super().__str__()

"""Managing classes"""

class PacMan(__Dict):
    """Class for managing used packages"""
    def __str__(self):
        text = ""
        for i in list(self):
            text += f"\\usepackage{str(i[1]) if i[1] else ''}{{{i[0]}}}"
        return text

class Master: # Дочерние элементы: класс документа, автор, название, дата, список пакетов, преамбула, документ (\begin{document}...\end{document})
    """Class for managing LaTeX document creation"""

    def __init__(self, document_class: DocumentClass = None, title: Title = None, authors: Authors = None, date: Date = None, packages: PacMan = None, document: Document = None):
        self.cls = document_class
        self.date = date
        self.title = title
        self.authors = authors
        self.packages = packages
        self.document = document

    def __str__(self) -> str:
        return f"{str(self.cls)}{str(self.packages)}"
