from .constants import one_of

class Ordered:
    order = 0

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.order = Ordered.order
        Ordered.order += 1
        return obj

class Field(Ordered):
    def __init__(self, size: int, convertor=None, start=None):
        self.size = size
        self.convertor = convertor
        self.start = start

        if isinstance(convertor, one_of):
            for attr, const in convertor.attrs.items():
                if attr in self.__dict__:
                    raise AttributeError(f'Constant cannot be stored as {attr!r}')
                if len(const.text) != self.size and convertor.size_check:
                    raise TypeError(f'{const!r} does not have a size of {self.size}')
                setattr(self, attr, const)

class Discriminator(Field):
    slice = slice(None, None)

    def __init__(self, text: str, *args, **kwargs):
        super().__init__(len(text), *args, **kwargs)
        self.text = text

    def __repr__(self):
        return f'<Discriminator {self.text!r} ({self.slice.start}-{self.slice.stop})>'

class Skip(Ordered):
    def __init__(self, size: int):
        self.size = size
