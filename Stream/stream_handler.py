from http.server import BaseHTTPRequestHandler, HTTPServer
import stream_generator
import ams
import stream_element_counter
import loglog
import hash_functions

__element_number = -1
moment_0 = 0
moment_1 = stream_generator.numbers_count  # we need to know count of numbers for AMS algorithm anyway
moment_2 = 0
ams_list_100 = ams.AMS(100, stream_generator.numbers_count)
ams_list_500 = ams.AMS(500, stream_generator.numbers_count)
precise_counter = stream_element_counter.StreamElementCounter()
loglog_md5 = loglog.LogLog(hash_functions.md5)
loglog_sha256 = loglog.LogLog(hash_functions.sha256)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        content_length = int(self.headers['Content-Length'])
        received_number = int(self.rfile.read(content_length).decode('utf-8'))
        self.__handle(received_number)

    @staticmethod
    def __handle(number: int):
        global moment_0, moment_2, __element_number
        __element_number += 1
        precise_counter.add_element(number)
        loglog_md5.process(number)
        loglog_sha256.process(number)
        # moment_1 += 1 # 1st moment is equal to count of all elements of stream
        ams_list_100.handle_item(__element_number, number)
        ams_list_500.handle_item(__element_number, number)

    @staticmethod
    def __output_results():
        print('0th moment (count of distinct elements):')
        print(f'Precise: {precise_counter.number_of_distinct()}')
        print(f'LogLog (MD5): {loglog_md5.get_result()}')
        print(f'LogLog (SHA256): {loglog_sha256.get_result()}')
        print('1st moment (count of elements):')
        print(moment_1)
        print('2nd moment:')
        print(f'Precise: {precise_counter.moment_2()}')
        print(f'AMS algorithm (100 variables): {ams_list_100.calculate_estimation()}')
        print(f'AMS algorithm (500 variables): {ams_list_500.calculate_estimation()}')


def start_handler():
    with HTTPServer(('', 8000), Handler) as server:
        server.serve_forever()
