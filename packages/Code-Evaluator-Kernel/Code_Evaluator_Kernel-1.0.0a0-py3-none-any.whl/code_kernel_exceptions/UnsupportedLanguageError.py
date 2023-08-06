class UnsupportedLanguageError(Exception):

    def __init__(self, language: str):
        self.message = f'{language} is not a valid language in kernel'

