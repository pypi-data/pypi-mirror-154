from lambdautility.vo.ResponseVO import ResponseVO

class MakeResponse:

    @staticmethod
    def success( errorMessage = None, data = None ):
        processResult = ResponseVO()
        processResult.errorTrace = "200 OK"
        processResult.errorCode = "000"
        processResult.errorMessage = (errorMessage, 'Proceso realizado correctamente.') [errorMessage==None]
        processResult.data = data
        return processResult
    
    @staticmethod
    def errorIncompleteRequestData( errorMessage=None, data=None ):
        processResult = ResponseVO()
        processResult.errorTrace = "400 Bad Request"
        processResult.errorCode = "100"
        processResult.errorMessage = (errorMessage, 'Los datos de la solicitud estan incompletos o son erroneos.') [errorMessage==None]
        processResult.data = data
        return processResult
        
    @staticmethod
    def errorNoSaldo( errorMessage=None, data=None ):
        processResult = ResponseVO()
        processResult.errorTrace = "400 Bad Request"
        processResult.errorCode = "100"
        processResult.errorMessage = (errorMessage,) [errorMessage==None]
        processResult.data = data
        return processResult
    
    @staticmethod
    def errorFailedConnectionBd( errorMessage=None, data=None ):
        processResult = ResponseVO()
        processResult.errorTrace = "500 Internal Server Error"
        processResult.errorCode = "200"
        processResult.errorMessage = (errorMessage, 'Imposible comunicarse con la Bd.') [errorMessage==None]
        processResult.data = data
        return processResult

    @staticmethod
    def errorException( errorMessage = None, data = None ):
        processResult = ResponseVO()
        processResult.errorTrace = "500 Internal Server Error"
        processResult.errorCode = "300"
        processResult.errorMessage = (errorMessage, 'Ocurrio una exception.') [errorMessage==None]
        processResult.data = data
        return processResult
    
    @staticmethod
    def errorAddRegBd( errorMessage = None, data = None ):
        processResult = ResponseVO()
        processResult.errorTrace = "500 Internal Server Error"
        processResult.errorCode = "300"
        processResult.errorMessage = (errorMessage, 'Error al agregar el registro en la tabla Logs.') [errorMessage==None]
        processResult.data = data
        return processResult
    
    @staticmethod
    def errorUpdateRegBd( errorMessage = None, data = None ):
        processResult = ResponseVO()
        processResult.errorTrace = "500 Internal Server Error"
        processResult.errorCode = "400"
        processResult.errorMessage = (errorMessage, 'Error al actualizar el registro en la tabla Logs.') [errorMessage==None]
        processResult.data = data
        return processResult
    
    @staticmethod
    def errorDeleteRegBd( errorMessage = None, data = None ):
        processResult = ResponseVO()
        processResult.errorTrace = "500 Internal Server Error"
        processResult.errorCode = "600"
        processResult.errorMessage = (errorMessage, 'Error al eliminar el registro en la tabla Logs.') [errorMessage==None]
        processResult.data = data
        return processResult
    
    @staticmethod
    def errorConsultingBd( errorMessage = None, data = None ):
        processResult = ResponseVO()
        processResult.errorTrace = "500 Internal Server Error"
        processResult.errorCode = "600"
        processResult.errorMessage = (errorMessage, 'Error al buscar el registro en la tabla Logs.') [errorMessage==None]
        processResult.data = data
        return processResult

class BadRequestException(Exception): pass
class NotFoundException(Exception): pass
class InternalServerError(Exception): pass
    