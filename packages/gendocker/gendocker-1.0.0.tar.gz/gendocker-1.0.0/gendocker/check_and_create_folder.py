import pathlib


def check_and_create_folder(target):
    pathlib.Path(target).mkdir(parents=True, exist_ok=True)
