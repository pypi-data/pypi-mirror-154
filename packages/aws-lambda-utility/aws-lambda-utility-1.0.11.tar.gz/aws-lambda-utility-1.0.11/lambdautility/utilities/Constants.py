'''
Created at 09 Jun 2022
Author: @juan.sanchezh
'''
import os

class Constants(object):

  ERROR_CODE_EXITO = "000"
  ERROR_CODE_CONTROLADO = "111"
  ERROR_CODE_EXCEPTION = "222"
  
  MESSAGE_EXITO = "SUCCESS"
  MESSAGE_WARNING = "WARNING"
  MESSAGE_CONTROLADO = "Ocurrío un error en la ejecución."
  MESSAGE_EXCEPTION = "ERROR"

  MESSAGE_IMPOSSIBLE_TO_COMMUNICATE_WITH_THE_DATABASE = 'Imposible comunicarse con la Bd.'
  MESSAGE_IMPOSSIBLE_TO_CLOSE_WITH_THE_DATABASE = 'Error al cerrar la conexión con la Bd.'
  MESSAGE_WHEN_ADDING_THE_RECORD_TO_THE_DATABASE = 'Error al insertar el registro en la Bd.'
  MESSAGE_WHEN_FIND_THE_RECORD_TO_THE_DATABASE = 'Error al consultar los datos en la Bd.'
  MESSAGE_WHEN_TRUNCATE_RECORDS_TO_THE_DATABASE = 'Error al eliminar los registros de la tabla en la Bd.'
  MESSAGE_WHEN_DROP_TABLE_TO_THE_DATABASE = 'Error al eliminar la tabla en la Bd.'
  MESSAGE_WHEN_RESPONSE_NULL = 'Error, no hubo resultados {mensaje}'
  MESSAGE_WHEN_PARAMETERS_ARE_NULL = 'Error, los campos {campos} son requeridos.'
  MESSAGE_SQS_EXITO = "Mensaje depositado en la queue satisfactoriamente"
  MESSAGE_SQS_CONTROLADO = "Ocurrió un error al depositar el mensaje"
  MESSAJE_ERROR_YA_APROVISIONADO = "Esta peticion ya ha sido presentada anteriormente."
  MESSAGE_ERROR_ORIGEN_NO_PROVIDER_DATA = "No se mandaron lineas para aprovisionar"
  MESSAGE_ERROR_ORIGEN_NO_VALIDO = "No existe el origen del cual se mando la peticion"
  MESSAGE_ERROR_SERVICIO_NOTFOUND = "El servicio {servicio} no se encuentra registrado en la base de datos"
  MESSAGE_ORIGEN_ERROR = "Error"
  MESSAGE_ERROR_EXCEPTION = "Ocurrio una exception"

  STATUS_SUCCESS = '200 OK'
  STATUS_BAD_REQUEST = '400 Bad Request'
  STATUS_INTERNAL_SERVER_ERROR = '500 Internal Server Error'
  
  SIEBEL_DATASOURCE = { "url" : os.getenv("SIEBEL_DATASOURCE") }
  LEGADOS_DATASOURCE = { "url" : os.getenv("LEGADOS_DATASOURCE") }
  EBSO_DATASOURCE = { "url" : os.getenv("EBSO_DATASOURCE") }
  APROV_DATASOURCE = { "url" : os.getenv("APROV_DATASOURCE") }
  APP_DATASOURCE = { "url" : os.getenv("APP_DATASOURCE") }
  BRM_DATASOURCE = { "url" : os.getenv("BRM_DATASOURCE") }
  AMAZON_DATASOURCE = { "url" : os.getenv("AMAZON_DATASOURCE") }
  DRP_DATASOURCE = { "url" : os.getenv("DRP_DATASOURCE")  }
  INTERNET_DATASOURCE = { "url" : os.getenv("INTERNET_DATASOURCE") }
  PAGOS_DATASOURCE = { "url" : os.getenv("PAGOS_DATASOURCE")  }

  FP_DATASOURCE = { "url" : os.environ.get("FP_DATASOURCE") }

  #Set Time Zone
  TIME_ZONE_MEXICO_CITY = 'America/Mexico_City'

  #InvokeLambda
  BOTO3_LAMBDA = 'lambda'
  #NAME_LAMBDA_APROV_ALPHA = os.environ['LAMBDA_APROV_BASE']
  TYPE_INVOCATION = 'RequestResponse'
  TYPE_ENCODE_UTF8 = 'UTF-8'

  #DynamoDB Client
  BOTO3_DYNAMODB = 'dynamodb'

  #SQS Invoke
  BOTO3_SQS = 'sqs'

  #CognitoIdentity Client
  BOTO3_COGNITO = 'cognito-identity'
  ENDPOINT = 'cognito-identity.amazonaws.com'

  #Environment
  ENVIRONMENT = os.getenv('ENVIRONMENT')
  IP = os.getenv('IP')
  SERVICE_HOST = os.getenv("ServiceHost")

  REQ_JSON_TEST = '"cuenta": "{cuenta}"'
  SQL_MYSQL_TEST = "select max(cliente_fp_compras_pk) as val from cliente_fp_compras_sku04"
  SQL_ORACLE_TEST = "select SMART_CARD from xbol_inv_asn_lines where SERIAL_NUMBER='{}'"


