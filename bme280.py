import weewx
from weewx.engine import StdService
import sys
import syslog

# Inherit from the base class StdService:
class bme(StdService):

    def __init__(self, engine, config_dict):
        # Pass the initialization information on to my superclass:
        super(bme, self).__init__(engine, config_dict)

        self.col_pres            =       config_dict['BME280']['col_pres']
        self.col_temp            =       config_dict['BME280']['col_temp']
        self.sl_denominator      = float(config_dict['BME280']['sl_denominator'])
        self.BME280_lib_location =       config_dict['BME280']['BME280_lib_location']

        # Bind to any new archive record events:
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_packet)

    def new_archive_packet(self, event):
        sys.path.insert(0, self.BME280_lib_location)
        from Adafruit_BME280 import *


        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()

        hectopascals = pascals / 100

        ## convert to sea level pressure
        ## relativePressure/(1-alt_in_meters/44330)^5.255
        ##
        ## we can read altitude of station, convert to m, then run the formala...
        ## for now I can just hard code that I have to divide by value in weewx.conf in my case
        hectopascals = hectopascals/self.sl_denominator

        pres_tuple = weewx.units.convertStd((hectopascals, "mbar", "group_pressure"), event.record['usUnits'])
        temp_tuple = weewx.units.convertStd((degrees, "degree_C", "group_temperature"), event.record['usUnits'])

        if self.col_pres:
            event.record[self.col_pres] = pres_tuple[0]
            syslog.syslog(syslog.LOG_INFO, "bme280: found pressure value of %s mbar" % pres_tuple[0])
        if self.col_temp:
            event.record[self.col_temp] = temp_tuple[0]
            syslog.syslog(syslog.LOG_INFO, "bme280: found temp value of %s" % temp_tuple[0])
