"""
A module for reading Analog to digital signals in a thread
"""
import logging
import threading
from time import sleep
import random
import os
import Queue
try:
    import Adafruit_ADS1x15                     
except ImportError:
    pass



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
        #  GAIN:   1 = +/-4.096V
        self.GAIN = 1
        # Create an ADS1115 ADC (16-bit) instance.
        if os.getenv('RESIN', 0):
            self.adc = Adafruit_ADS1x15.ADS1115(busnum=1)
        else:
            self.adc = None

    def _read_adc_values(self):
        if os.getenv('RESIN', 0):
            # read from real ADC
            readings = [0, 0, 0, 0]
            for index, value in enumerate(readings):
                readings[index] = self.adc.read_adc(index, gain=self.GAIN)
            return readings
        else:
            # Generate random ADC readings
            readings = [0, 0, 0, 0]
            for index, value in enumerate(readings):
                print "index = " + str(index)
                readings[index] = random.randint(0, 4096)
            return readings

    def _avg_adc_values(self, readings=5):
        s = [0, 0, 0, 0]
        for i in range(0, readings):
            logging.debug(s)
            s = [x + y for x, y in zip(s, self._read_adc_values())]
            sleep(0.025)
        return [s / readings for s in s]

    def run(self):
        logging.debug("Starting ADC thread")
        while not self.stopper.is_set():
            logging.debug("reading from ADC")
            adc_values = self._avg_adc_values()
            try:
                self.q.put_nowait(adc_values)
                logging.debug(adc_values)
                logging.debug(values_to_voltages(adc_values))
            except Queue.Full:
                logging.debug("queue is full, dropping values")

            sleep(self.interval)

def values_to_voltages(values):
    return [float(i)*0.000124627063 for i in values]