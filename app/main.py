"""
Main.py
"""
import logging
import signal
import threading
from time import sleep
import Queue

from adc import Adc
from utils import SignalHandler

def main():
    """
    The entry point for our program
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info('Started')
    stopper = threading.Event()
    adc_queue = Queue.Queue(10)

    # Setup our input threads
    adc_thread = Adc(adc_queue, 0.5, stopper)

    # create our signal handler and connect it
    handler = SignalHandler(stopper, [adc_thread])
    signal.signal(signal.SIGINT, handler)

    adc_thread.start()

    while True:
        logging.info("running in main loop...")
        try:
            logging.debug(adc_queue.qsize())
            adc_value = adc_queue.get_nowait()
            logging.info(adc_value)
        except Queue.Empty:
            logging.debug("adcQueue is empty")
        sleep(0.25)

if __name__ == '__main__':
    main()
