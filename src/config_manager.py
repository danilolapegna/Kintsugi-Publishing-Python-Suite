#!/usr/bin/env python3

"""
ConfigManager handles loading, retrieving, and overriding values 
from a YAML configuration file. It supports nested key access 
using dot notation and allows runtime overrides.
"""

import yaml
import os

class ConfigManager:
    def __init__(self, config_path: str):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(script_dir, '..'))
        full_path = os.path.join(base_dir, config_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(full_path)
        with open(full_path, 'r', encoding='utf-8') as file:
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