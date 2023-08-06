import os


def delete_temp_file(filepath: str):
    os.remove(filepath)
