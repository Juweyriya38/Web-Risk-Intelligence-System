"""
Configuration loader with validation.
Loads and validates settings.yaml at startup.
"""

import yaml
from pathlib import Path
from typing import Optional
from app.core.models import ConfigurationSchema


class ConfigLoader:
    """Loads and validates configuration from YAML."""

    _instance: Optional[ConfigurationSchema] = None

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> ConfigurationSchema:
        """
        Load configuration from YAML file.

        Args:
            config_path: Optional custom config path

        Returns:
            Validated configuration schema

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "settings.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, "r") as f:
            raw_config = yaml.safe_load(f)

        try:
            config = ConfigurationSchema(**raw_config)
            config.validate_config()
            cls._instance = config
            return config
        except Exception as e:
            raise ValueError(f"Invalid configuration: {e}") from e

    @classmethod
    def get_instance(cls) -> ConfigurationSchema:
        """Get cached configuration instance."""
        if cls._instance is None:
            raise RuntimeError("Configuration not loaded. Call load() first.")
        return cls._instance
