def get_project_config(project_name, configs):
    config = list(filter(lambda item: item["name"] == project_name, configs))[0]
    return config
