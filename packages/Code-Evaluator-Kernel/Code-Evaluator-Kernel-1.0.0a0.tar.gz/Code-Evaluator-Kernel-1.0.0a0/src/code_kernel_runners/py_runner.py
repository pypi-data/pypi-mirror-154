from code_kernel_utils.process_utils import run_code


def run_py(filepath: str, inputs: [str]) -> [str]:
    return run_code('python', [filepath], inputs)
