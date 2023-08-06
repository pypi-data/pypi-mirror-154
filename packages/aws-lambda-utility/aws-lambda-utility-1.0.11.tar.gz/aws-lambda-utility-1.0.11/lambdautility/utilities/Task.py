'''
Created at 09 Jun 2022
Author: @juan.sanchezh
'''

import json, logging, requests
from lambdautility.utilities.Constants import Constants
from lambdautility.conn.aws.Connection import getConnectionLambda, getConnectionSqs

logging.basicConfig(level=logging.INFO)

def getBodyJson(body):
    jsonBody = None
    try:
        jsonBody = (json.loads('{'+body+'}'))
    except Exception as e:
        jsonBody = None
        logging.error("Ex Task.getBodyJson: " + str(e))
    return jsonBody

def ejecutarServicioREST(body, url, aut):
    responseWs = None
    try:
        logging.info("Task.ejecutarServicioREST.request: " + str(url) + " :: " + str(body) )
        
        if aut is None:
            headers = {"Content-Type": "application/json"} 
        else: 
            headers = {"Content-Type": "application/json", "openid": aut.getOpenIdToken} 
            
        respWs = requests.post(url, data = json.dumps(body), headers = headers)
        #print(type(respWs), respWs.headers)
        if respWs.status_code != 201:
            responseWs = respWs.json()
            logging.info("Task.ejecutarServicioREST.response: " + str(responseWs))
    except Exception as e:
        responseWs = None
        logging.error("Ex Task.ejecutarServicioREST: " + str(e))
        raise Exception(str(e))
    return responseWs
    
def invokeLambda(data, lambda_name):
        response = None
        mensaje = None
        try:
            mensaje = data
            payload = json.dumps(mensaje)
            logging.info("Task.invokeLambda.requestLambda: " + str(payload))
            client = getConnectionLambda()
            responseLambda = client.invoke(
                FunctionName = lambda_name,
                InvocationType = Constants.TYPE_INVOCATION,
                Payload = bytes(payload, encoding = Constants.TYPE_ENCODE_UTF8)
            )
            response = json.loads(responseLambda['Payload'].read())
            logging.info("Task.invokeLambda.responseLambda: " + str(response))
            return response
        except Exception as e:
            logging.error("Ex Task.invokeLambda: " + str(e))
            raise Exception('Exception: No se pudo invocar la lambda' + str(e))
        return response

def sendMessageSQS(message, sqs_name):
        response = None
        try:
            sqs = getConnectionSqs()
            queue_name = sqs_name
            queue = sqs.get_queue_by_name(QueueName=queue_name)
            response = queue.send_message(
                    MessageBody=(json.dumps(message, ensure_ascii=False))
                )
            
            if len(response.get('MessageId')) > 0:
                logging.info(Constants.MESSAGE_SQS_EXITO)
                logging.info("MessageId: " + str(response['MessageId']))
                logging.info("MD5OfMessageBody: " + str(response['MD5OfMessageBody']))
            else:
                raise Exception(Consctants.MESSAGE_SQS_CONTROLADO)
        except Exception as e:
            logging.info("Ex Task.sendMessageSQS : " + str(e))
            raise e
        return response