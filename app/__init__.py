import pathlib
from core.configuration import Configuration

# load the application configuration
configuration = Configuration.from_yaml(str(pathlib.Path(".") / "config.yaml"))