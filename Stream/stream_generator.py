import requests
import random
import time

numbers_count = 1000000
__min_number = 0
__max_number = 1000
__time_between_numbers = 0.2


def generate():
    time.sleep(1)
    print('Number generator started')
    for i in range(numbers_count):
        requests.post('http://127.0.0.1:8000', data=str(random.randint(__min_number, __max_number)))
        time.sleep(__time_between_numbers)
