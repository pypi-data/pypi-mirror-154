import logging
from time import time

logging.basicConfig(level=logging.INFO)  #definimos el nivel en el cual queremos se muestre la informacion en la consola

def init(funcion):
    def setExecutionTime(*args, **kwargs):
        logging.info(f"Inicio de la ejecución");
        logging.info(args)
        processTime = time()
        funcion(*args, **kwargs)
        processTime = time() - processTime
        logging.info(f"Fin de la ejecución {processTime}");
    return setExecutionTime