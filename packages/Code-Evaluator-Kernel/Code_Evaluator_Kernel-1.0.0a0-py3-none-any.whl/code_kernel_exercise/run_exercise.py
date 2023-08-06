from code_kernel_utils.language_utils import get_runner
from code_kernel_exceptions.CompilationError import CompilationError
from code_kernel_exceptions.ExecutionError import ExecutionError
from code_kernel_exceptions.CodeTimeoutError import CodeTimeoutError
from code_kernel_file_handling.create_temp_file import create_temp_file
from code_kernel_exceptions.UnsupportedLanguageError import UnsupportedLanguageError
from code_kernel_config.supported_languages import is_not_supported
from code_kernel_exceptions.CodeKernelException import CodeKernelException


status: [str] = ['PASSED', 'FAILED', 'COMPILATION_ERROR', 'EXECUTION_ERROR', 'TIMEOUT_ERROR','LANGUAGE_NOT_SUPPORTED']


def run_exercise(language: str, solution: str, inputs: [str], outputs: [str]) -> (str, [str]):
    try:
        if is_not_supported(language):
            raise UnsupportedLanguageError(language)

        filename = create_temp_file(solution, language)

        results = get_runner(language)(filename, inputs)

        if outputs == results:
            return status[0], results
        else:
            return status[1], results

    except CompilationError:
        return status[2], []

    except ExecutionError:
        return status[3], []

    except CodeTimeoutError:
        return status[4], []

    except UnsupportedLanguageError:
        raise UnsupportedLanguageError(language)

    except Exception as exception:
        raise CodeKernelException(exception)

