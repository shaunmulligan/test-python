"""
A module for reading Analog to digital signals in a thread
"""
import logging
import threading
from time import sleep
import random
import Queue

class Adc(threading.Thread):
    """
    The thread that will read analog to digital values.
    """
    #: An event that tells the thread to stop
    stopper = None

    def __init__(self, q, interval, stopper):
        threading.Thread.__init__(self)
        self.stopper = stopper # bool to stop thread
        self.q = q # shared queue of values
        self.interval = interval # interval between measurements ()
        # TODO: create an instance of ADS1x15 with i2c bus number set in instance creation.

    def _read_adc_value(self):
        # TODO: Get actual ADC value here.
        return random.randint(0, 4096)

    def _avg_adc_value(self, readings=5):
        s = 0
        for i in range(0, readings):
            s = s + self._read_adc_value()
            sleep(0.025)
        return s/readings
    
    def run(self):
        logging.debug("Starting ADC thread")
        while not self.stopper.is_set():
            logging.debug("reading from ADC")
            adc_value = self._avg_adc_value()
            try:
                self.q.put_nowait(adc_value)
                logging.debug(adc_value)
            except Queue.Full:
                logging.debug("queue is full, dropping values")

            sleep(self.interval)
