#permite que nuestro paquete se pueda ejecutar fuera por otra aplicación/usuario

from lambdautility import Constants
from lambdautility import init
from lambdautility import getDateCurrentStr, getDateStr, getDateTimeCurrentBd, getDateStrSumDays
from lambdautility import MakeResponse
from lambdautility import ejecutarServicioREST, getBodyJson, invokeLambda, sendMessageSQS
from lambdautility import getConnectionDynamoDb
from lambdautility import getConnectionOracleDataSourceByOrigin, closeConnectionOracle, getConnectionMySqlDataSourceByOrigin, closeConnectionMysql
from jsonUtils import rowsToList
import logging, os


#cuando usamos el modulo logging, solo el tipo warning, error, critical sera mostrado en consola

#si queremos que se muestre desde algún nivel en particular, debemos especificarlo en el método basicConfig

logging.basicConfig(level=logging.INFO)


def main():
  logging.info('El valor para name desde __main__.py es: {}'.format(__name__))
  # logging.info(getProximosCursos.__doc__)
  # logging.info(getProximosCursos())


# ejecuta todo el código que esté dentro, solo si este archivo se ejecuta como programa principal
if __name__ == '__main__':
  logging.info('Ejecución del paquete')
  main()
  logging.info('Fin de la ejecución del paquete')