class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int,
    ):
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class DocumentNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="Document not found.",
            status_code=404,
        )


class AIServiceRateLimitException(AppException):
    def __init__(self):
        super().__init__(
            message="AI service quota exceeded. Please try again later.",
            status_code=429,
        )


class InvalidFileTypeException(AppException):
    def __init__(self):
        super().__init__(
            message="Unsupported file type.",
            status_code=400,
        )


class EmptyFileException(AppException):
    def __init__(self):
        super().__init__(
            message="The uploaded file is empty.",
            status_code=400,
        )

class FileTooLargeException(AppException):
    def __init__(self):
        super().__init__(
            message="Uploaded file exceeds the maximum allowed size.",
            status_code=413,
        )