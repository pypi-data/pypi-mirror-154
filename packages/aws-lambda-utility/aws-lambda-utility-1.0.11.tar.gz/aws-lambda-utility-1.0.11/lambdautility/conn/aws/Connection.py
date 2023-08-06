'''
Created at 09 Jun 2022
Author: @juan.sanchezh
'''

import boto3, logging
from lambdautility.utilities.Constants import Constants

logging.basicConfig(level=logging.INFO)

def getConnectionLambda():
    connection = None
    try:
        connection = boto3.client(Constants.BOTO3_LAMBDA)
    except Exception as e:
        connection = None
        logging.error("Ex Connection.getConnectionLambda: " + str(e))
        raise Exception("Lambda access problem")
    return connection

def getConnectionDynamoDb():
    connection = None
    try:
        connection = boto3.resource(Constants.BOTO3_DYNAMODB)
    except Exception as e:
        connection = None
        logging.error("Ex Connection.getConnectionDynamoDb: " + str(e))
        raise Exception("DynamoDb access problem")
    return connection

def getConnectionSqs():
    connection = None
    try:
        connection = boto3.resource(Constants.BOTO3_SQS)
    except Exception as e:
        connection = None
        logging.error("Ex Connection.getConnectionSqs: " + str(e))
        raise Exception("Sqs access problem")
    return connection