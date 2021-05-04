from http.server import BaseHTTPRequestHandler, HTTPServer
import stream_generator
import ams
import stream_element_counter
import loglog
import hash_functions
import sys
import time

handled_elements = 0
server: 'Handler'
moment_0 = 0
moment_1 = stream_generator.numbers_count  # we need to know count of numbers for AMS algorithm anyway
moment_2 = 0
ams_list_100 = ams.AMS(100, stream_generator.numbers_count)
ams_list_500 = ams.AMS(500, stream_generator.numbers_count)
precise_counter = stream_element_counter.StreamElementCounter()
loglog_md5 = loglog.LogLog(hash_functions.md5)
loglog_sha256 = loglog.LogLog(hash_functions.sha256)
loglog_linear = loglog.LogLog(hash_functions.linear)
t = 0


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global t
        t = time.perf_counter()
        self.send_response(200)
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length).decode('utf-8')
        #print(content)
        received_number = int(content)
        print(f"Server received number {received_number}")
        self.__handle(received_number)
        print(time.perf_counter() - t)

    # def do_GET(self):
    #     self.send_response(200)

    @staticmethod
    def __handle(number: int):
        global moment_0, moment_2, handled_elements
        handled_elements += 1
        precise_counter.add_element(number)
        loglog_md5.process(number)
        loglog_sha256.process(number)
        loglog_linear.process(number)
        # moment_1 += 1 # 1st moment is equal to count of all elements of stream
        ams_list_100.handle_item(handled_elements, number)
        ams_list_500.handle_item(handled_elements, number)
        print(f'Current element number: {handled_elements}')
        if handled_elements >= stream_generator.numbers_count:
            Handler.__finalize()

    @staticmethod
    def __finalize():
        server.server_close()
        with open('results.txt', 'a') as f:
            print('0th moment (count of distinct elements):', file=f)
            print(f'Precise: {precise_counter.number_of_distinct()}', file=f)
            print(f'LogLog (MD5): {loglog_md5.get_result()}', file=f)
            print(f'LogLog (SHA256): {loglog_sha256.get_result()}', file=f)
            print(f'LogLog (linear function): {loglog_linear.get_result()}', file=f)
            print('1st moment (count of elements):', file=f)
            print(moment_1, file=f)
            print('2nd moment:', file=f)
            print(f'Precise: {precise_counter.moment_2()}', file=f)
            print(f'AMS algorithm (100 variables): {ams_list_100.calculate_estimation()}', file=f)
            print(f'AMS algorithm (500 variables): {ams_list_500.calculate_estimation()}', file=f)
            sys.exit(0)


def start_handler():
    print('Starting server...')
    global server
    server = HTTPServer(('127.0.0.1', 8000), Handler)
    # with HTTPServer(('127.0.0.1', 8000), Handler) as server:
    server.serve_forever()
