import tempfile

from code_kernel_config.supported_languages import supported_languages


def create_temp_file(body: str, language: str) -> str:
    extension = supported_languages[language]['extension']
    file = tempfile.NamedTemporaryFile(mode='w', suffix=f'.{extension}', delete=False)
    filename = file.name
    file.write(body)
    file.close()
    return filename
