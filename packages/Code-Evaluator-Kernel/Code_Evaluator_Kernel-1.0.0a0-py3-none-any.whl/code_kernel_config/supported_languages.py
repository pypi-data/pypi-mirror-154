from code_kernel_runners.cpp_runner import run_cpp
from code_kernel_runners.py_runner import run_py

supported_languages = {
    'c++': {
        'extension': 'cpp',
        'run': run_cpp
    },
    'python': {
        'extension': 'py',
        'run': run_py
    }

}


def is_not_supported(language: str) -> bool:
    return language not in supported_languages
