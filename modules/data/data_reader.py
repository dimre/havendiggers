"""Read data from files"""
import os
import re
import yaml


def get_abs_path(*root_file_path: str) -> str:
    r"""Get the abs path from the root directory of the project to the requested path

    Args:
        root_file_path (\*str): path from the root project directory

    Returns:
        str: corrisponding abs path
    """
    root_path = os.path.join(os.path.dirname(__file__), "..", "..")
    return os.path.join(root_path, *root_file_path)


def read_file(*root_file_path: str) -> str:
    r"""Read the contens of the file

    Args:
        root_file_path (\*str): path of the file to read from the root project directory

    Returns:
        str: contents of the file
    """
    with open(get_abs_path(*root_file_path), "r", encoding="utf-8") as in_file:
        text = in_file.read().strip()
    return text


def read_md(file_name: str) -> str:
    """Read the contens of a markdown file.
    The path is data/md.

    Args:
        file_name (str): name of the file

    Returns:
        str: contents of the file
    """
    return read_file("data", "md", file_name + ".md")


def read_env(config: dict):
    """Reads the enviroment variables

    Args:
        config: config_map
    """
    new_vars = {}
    config['test'] = config['test'] if config.get('test', False) else {}
    if os.path.exists(get_abs_path(".env")):
        envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')
        with open(get_abs_path(".env")) as env:
            for line in env:
                match = envre.match(line)
                if match is not None:
                    new_vars[match.group(1).lower()] = match.group(2)

    var_keys = ("TELEGRAM_TOKEN", "TWITTER_API_KEY", "TWITTER_API_KEY_SECRET", "TWITTER_ACCESS_TOKEN",
                "TWITTER_ACCESS_TOKEN_SECRET")
    for key in var_keys:
        if (var := os.getenv(key)) is not None:
            new_vars[key.lower()] = var

    for key in new_vars:
        if key.startswith("test_"):
            config['test'][key[5:]] = new_vars[key]
        else:
            config[key] = new_vars[key]


# Reads the configuration of the bot
with open(get_abs_path("config", "settings.yaml"), 'r', encoding="utf-8") as yaml_config:
    config_map = yaml.load(yaml_config, Loader=yaml.SafeLoader)
read_env(config_map)
