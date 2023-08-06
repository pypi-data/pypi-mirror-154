class ResponseVO:
    def __init__(self):
        self.__errorCode=None
        self.__errorMessage=None
        self.__errorTrace=None
        self.__data=None
        self.__timeResponse = None
        self.__dateResponse = None
        self.__exception = None
        
    @property
    def errorCode(self):
        return self.__errorCode
    
    @errorCode.setter
    def errorCode(self, value):
        self.__errorCode = value
    
    @property
    def errorMessage(self):
        return self.__errorMessage
    
    @errorMessage.setter
    def errorMessage(self, value):
        self.__errorMessage = value

    @property
    def errorTrace(self):
        return self.__errorTrace
    
    @errorTrace.setter
    def errorTrace(self, value):
        self.__errorTrace = value
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def timeResponse(self):
        return self.__timeResponse
    
    @timeResponse.setter
    def timeResponse(self, timeResponse):
        self.__timeResponse = timeResponse

    @property
    def dateResponse(self):
        return self.__dateResponse
    
    @dateResponse.setter
    def dateResponse(self, value):
        self.__dateResponse = value
    
    @property
    def exception(self):
        return self.__exception
    
    @exception.setter
    def exception(self, value):
        self.__exception = value

    def getDictionary(self):
        return {
            "control": {
                "errorCode": str(self.__errorCode),
                "errorMessage": str(self.__errorMessage),
                "errorTrace": str(self.__errorTrace),
                "timeResponse" : str(self.__timeResponse),
                "dateResponse" : str(self.__dateResponse),
                "exception" : self.__exception
            },
            "data": self.__data
        }