from functools import reduce


class StreamElementCounter:
    def __init__(self):
        self.__elements: dict[..., int] = {}

    def add_element(self, element):
        if element in self.__elements:
            self.__elements[element] += 1
        else:
            self.__elements[element] = 1

    def number_of_distinct(self):
        return len(self.__elements)

    def moment_2(self):
        return reduce(lambda result, element: result + element * element, self.__elements.values(), 0)
