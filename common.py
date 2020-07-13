import yaml


def yaml_load(name):
    with open(name) as stream:
        param = yaml.safe_load(stream)
    return param
