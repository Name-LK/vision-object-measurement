# Functions to load config.yaml configurations
import yaml

def load_config(path: str = 'config.yaml'):
    """Load the YAML config file

    Args:
        path (str, optional): Config Path. Defaults to 'config.yaml'.
    """
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file not found at {path}")