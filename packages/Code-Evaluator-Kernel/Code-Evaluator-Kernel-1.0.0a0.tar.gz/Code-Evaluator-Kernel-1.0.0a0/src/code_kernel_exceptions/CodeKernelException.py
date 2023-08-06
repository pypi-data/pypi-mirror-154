class CodeKernelException(Exception):

    def __init__(self, message):
        self.message = f'An error occurred - details {message}'

