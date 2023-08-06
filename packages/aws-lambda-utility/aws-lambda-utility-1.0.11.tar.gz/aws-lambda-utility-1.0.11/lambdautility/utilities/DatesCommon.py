import logging
import pytz
import datetime
import json
from lambdautility.utilities.Constants import Constants

logging.basicConfig(level=logging.INFO)

def getDateCurrentStr():
    fecha = None
    try:
        timezone = pytz.timezone(Constants.TIME_ZONE_MEXICO_CITY)
        fecha = datetime.datetime.now(timezone)
        fecha = "{0:%d-%m-%Y %H:%M:%S}".format(fecha)
    except Exception as ex:
        logging.error('Ex al obtener la hora y fecha actual y transformarla a string. DatesCommon.getDateCurrentStr')
        logging.error(ex)
            
    return fecha

def getDateStr():
    fecha = None
    try:
        timezone = pytz.timezone(Constants.TIME_ZONE_MEXICO_CITY)
        fecha = datetime.datetime.now(timezone)
        fecha = "{0:%Y-%m-%d}".format(fecha)
    except Exception as ex:
        logging.error('Ex al obtener la fecha actual y transformarla a string. DatesCommon.getDateStr')
        logging.error(ex)
            
    return fecha

def getDateTimeCurrentBd():
    fecha = None
    try:
        timezone = pytz.timezone(Constants.TIME_ZONE_MEXICO_CITY)
        fecha = f"{datetime.datetime.now(timezone):%Y-%m-%d %H:%M:%S}"
    except Exception as ex:
        logging.error('Ex al obtener la hora y fecha actual del sistema')
        logging.error(ex)
            
    return fecha
    
def getDateStrSumDays(dias):
    fecha = None
    try:
        timezone = pytz.timezone(Constants.TIME_ZONE_MEXICO_CITY)
        fecha = datetime.datetime.now(timezone) + datetime.timedelta(days=dias)
        fecha = "{0:%Y-%m-%d}".format(fecha)
    except Exception as ex:
        logging.error('Ex al obtener la fecha actual y transformarla a string. DatesCommon.getDateStr')
        logging.error(ex)
    return fecha
    
