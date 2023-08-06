from code_kernel_exercise.run_exercise import run_exercise


def begin_evaluation(language: str, solution: str, inputs: [str], outputs: [str]) -> dict:

    status, results = run_exercise(language, solution, inputs, outputs)

    overview = {
        'status': status,
        'expected': outputs,
        'got': results
    }

    return overview

