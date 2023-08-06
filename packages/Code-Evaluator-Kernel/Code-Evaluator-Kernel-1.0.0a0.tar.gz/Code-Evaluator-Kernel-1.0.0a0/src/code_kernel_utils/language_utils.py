from code_kernel_config.supported_languages import supported_languages
from code_kernel_exceptions.UnsupportedLanguageError import UnsupportedLanguageError


def is_supported_language(language: str) -> bool:
    return language in supported_languages


def get_file_extension(language: str) -> str:
    if is_supported_language(language):
        return supported_languages[language]['extension']
    else:
        raise UnsupportedLanguageError(language)


def get_runner(language: str) -> lambda: [str]:
    if is_supported_language(language):
        return supported_languages[language]['run']
    else:
        raise UnsupportedLanguageError(language)
