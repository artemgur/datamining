import random


class AMS:
    def __init__(self, count: int, stream_length: int):
        self.__list = [random.randint(0, stream_length - 1) for i in range(count)]
        self.__list.sort()
        self.__counted_values: dict[int, list[int]] = {}
        self.__current_index = 0
        self.__stream_length = stream_length

    def handle_item(self, index: int, value: int):
        while self.__current_index < len(self.__list) and index == self.__list[self.__current_index]:
            self.__counted_values[index].append(1)
            self.__current_index += 1
        if value in self.__counted_values:
            for i in range(len(self.__counted_values[value])):
                self.__counted_values[value][i] += 1

    def calculate_estimation(self):
        repetition_number_list = [x for i in self.__counted_values.items() for x in i] # TODO type?
        repetition_number_list = map(lambda x: self.__stream_length * (2 * x - 1), repetition_number_list)
        list_sum = sum(repetition_number_list)
        return list_sum / self.__stream_length
