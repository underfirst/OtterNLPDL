class ErrorMessage:
    def __init__(self):
        self.messages = list()

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        self.messages.append(value)

    def __getattr__(self, key):
        message = self.__dict__[key]
        idx = self.messages.index(message)
        return f"{idx}: {message}"

error_message = ErrorMessage()
error_message.fail_fit = "Fail train.fit"