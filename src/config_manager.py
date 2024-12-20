import yaml
import os

class ConfigManager:
    def __init__(self, config_path: str):
        if not os.path.exists(config_path):
            raise FileNotFoundError(config_path)
        with open(config_path, 'r', encoding='utf-8') as file:
            self._config = yaml.safe_load(file) or {}

    def get(self, key: str, default=None):
        parts = key.split(".")
        node = self._config
        for part in parts:
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def override(self, key: str, value):
        if value is None:
            return
        parts = key.split(".")
        node = self._config
        for part in parts[:-1]:
            if part not in node:
                node[part] = {}
            node = node[part]
        node[parts[-1]] = value
