import json
import os
from typing import Dict, List, Any

DEFAULT_CONFIG = {
    'notification_channel': 0,
    'role_to_mention': 0,
    'secs_between_ping': 60,
}

# Default servers list
DEFAULT_SERVERS = [
    {
        'name': 'Example Server',
        'address': 'example.com'
    }
]

# File paths
CONFIG_FILE = 'config.json'
SERVERS_FILE = 'servers.json'


def load_json(file_path: str, default_data: Any) -> Any:
    """
    Load JSON data from a file, creating it with default data if it doesn't exist

    Args:
        file_path (str): Path to the JSON file
        default_data (Any): Default data to use if file doesn't exist

    Returns:
        Any: Loaded data
    """
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(default_data, f, indent=4)
            return default_data

        with open(file_path, 'r') as f:
            return json.load(f)

    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return default_data


def save_json(file_path: str, data: Any) -> bool:
    """
    Save data to a JSON file

    Args:
        file_path (str): Path to the JSON file
        data (Any): Data to save

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False


def get_config() -> Dict[str, Any]:
    """
    Get the current configuration

    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    return load_json(CONFIG_FILE, DEFAULT_CONFIG)


def get_servers() -> List[Dict[str, str]]:
    """
    Get the list of servers to monitor

    Returns:
        List[Dict[str, str]]: List of server dictionaries
    """
    return load_json(SERVERS_FILE, DEFAULT_SERVERS)


def save_config(config_data: Dict[str, Any]) -> bool:
    """
    Save the configuration

    Args:
        config_data (Dict[str, Any]): Configuration to save

    Returns:
        bool: True if successful, False otherwise
    """
    return save_json(CONFIG_FILE, config_data)


def save_servers(servers_data: List[Dict[str, str]]) -> bool:
    """
    Save the list of servers

    Args:
        servers_data (List[Dict[str, str]]): Servers data to save

    Returns:
        bool: True if successful, False otherwise
    """
    return save_json(SERVERS_FILE, servers_data)


def update_config() -> tuple:
    """
    Reload configuration from files

    Returns:
        tuple: (servers, config) tuple with fresh data
    """
    return get_servers(), get_config()
