import os


def get_folder_list(configs):
    project_list = [config["name"] for config in configs]
    folder_list = [name for name in os.listdir("../")]
    available_list = [name for name in project_list if name in folder_list]
    return available_list
