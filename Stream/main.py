import stream_handler
import stream_generator
from multiprocessing import Process

#stream_handler.start_handler()
process = Process(target=stream_handler.start_handler)
process.start()

stream_generator.generate()
