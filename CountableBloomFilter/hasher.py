import random


class Hasher:
    #Hash functions are linear, ax+b
    __min_a = 10000
    __max_a = 20000

    __min_b = 10000
    __max_b = 20000

    def __init__(self):
        r = random.Random()
        self.__a = r.randint(Hasher.__min_a, Hasher.__max_a)
        self.__b = r.randint(Hasher.__min_b, Hasher.__max_b)

    def hash(self, s: str) -> int:
        return self.__a * hash(s) + self.__b