'''
Created at 09 Jun 2022
Author: @juan.sanchezh
'''

import logging, alchemyHelper, os, sys, cx_Oracle
from sqlalchemy import create_engine
from lambdautility.utilities.Constants import *

if sys.platform.startswith("win"):
    cx_Oracle.init_oracle_client(lib_dir=r"F:\paquetes\oracle\instantclient_21_3")

if not sys.platform.startswith("win"):
    with open('/tmp/HOSTALIASES', 'w') as hosts_file:hosts_file.write('{} localhost\n'.format(os.uname()[1]))

logging.basicConfig(level=logging.INFO)
#class Connection(object): 
def getConnectionOracleDataSourceByOrigin(origen, logger):
    connection = None
    try:
        if origen == "SIEBEL":
            dataSource = Constants.SIEBEL_DATASOURCE["url"]
        elif origen == "LEGADOS":
            dataSource = Constants.LEGADOS_DATASOURCE["url"]
        elif origen == "EBSO":
            dataSource = Constants.EBSO_DATASOURCE["url"]
        elif origen == "PAGOS":
            dataSource = Constants.PAGOS_DATASOURCE["url"]
        elif origen == "APROV":
            dataSource = Constants.APROV_DATASOURCE["url"]
        elif origen == "APP":
            dataSource = Constants.APP_DATASOURCE["url"]
        elif origen == "BRM":
            dataSource = Constants.BRM_DATASOURCE["url"]
        elif origen == "AMAZON":
            dataSource = Constants.AMAZON_DATASOURCE["url"]
        elif origen == "DRP":
            dataSource = Constants.DRP_DATASOURCE["url"]
        elif origen == "INTERNET":
            dataSource = Constants.INTERNET_DATASOURCE["url"]
        elif origen == "PAGOS":
            dataSource = Constants.PAGOS_DATASOURCE["url"] 

        connection = create_engine(dataSource).connect().execution_options(autocommit=True)
    except Exception as e:
        logger.error("Ex Connection.getConnectionOracle: " + str(e))
        raise Exception("Database access problem: " + str(Constants.MESSAGE_IMPOSSIBLE_TO_COMMUNICATE_WITH_THE_DATABASE))
    return connection
    
def closeConnectionOracle(connection):
    try:
        if connection is not None:
            connection.close()
            #logging.info("Conexion cerrada")
    except Exception as e:
        logging.error("Ex Connection.closeConnectionOracle: " + str(e))
        raise Exception("Database close problem: " + str(Constants.MESSAGE_IMPOSSIBLE_TO_CLOSE_WITH_THE_DATABASE))

def getConnectionMySqlDataSourceByOrigin(origen, logger):
    connection = None
    try:
        if origen == "FP":
            dataSource = Constants.FP_DATASOURCE["url"]
            
        connection = alchemyHelper.getEngine(dataSource).connect()
    except Exception as e:
        logger.error("Ex Connection.getConnectionMySql: " + str(e))
        raise Exception("Database access problem: " + str(Constants.MESSAGE_IMPOSSIBLE_TO_COMMUNICATE_WITH_THE_DATABASE) + " MySQL")
    return connection

def closeConnectionMysql(connection):
    try:
        if connection is not None:
            connection.close()
            #logging.info("Conexion cerrada")
    except Exception as e:
        logging.error("Ex Connection.closeConnectionMysql: " + str(e))
        raise Exception("Database close problem: " + str(Constants.MESSAGE_IMPOSSIBLE_TO_CLOSE_WITH_THE_DATABASE) + " MySQL")