"""
Configuration and secrets management utility.

This module provides functionality to load configuration and secrets from YAML files
in a secure and organized manner.
"""

import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """
    Manages configuration and secrets loading from YAML files.
    """
    
    def __init__(self, secrets_file: str = "secrets.yaml", config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            secrets_file: Path to the secrets YAML file
            config_file: Optional path to a separate config YAML file
        """
        self.project_root = self._find_project_root()
        self.secrets_file = Path(self.project_root) / secrets_file
        self.config_file = Path(self.project_root) / config_file if config_file else None
        self._secrets = None
        self._config = None
    
    def _find_project_root(self) -> Path:
        """Find the project root directory by looking for .gitignore or other markers."""
        current = Path.cwd()
        
        # Look for project markers
        markers = ['.gitignore', 'secrets.example.yaml', 'README.md']
        
        while current != current.parent:
            if any((current / marker).exists() for marker in markers):
                return current
            current = current.parent
        
        # Fallback to current directory
        return Path.cwd()
    
    def load_secrets(self) -> Dict[str, Any]:
        """
        Load secrets from the YAML file.
        
        Returns:
            Dictionary containing all secrets
            
        Raises:
            FileNotFoundError: If secrets file doesn't exist
            yaml.YAMLError: If YAML file is malformed
        """
        if self._secrets is None:
            if not self.secrets_file.exists():
                raise FileNotFoundError(
                    f"Secrets file not found: {self.secrets_file}\n"
                    f"Please copy secrets.example.yaml to secrets.yaml and fill in your values."
                )
            
            with open(self.secrets_file, 'r') as f:
                self._secrets = yaml.safe_load(f)
        
        return self._secrets
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the YAML file.
        
        Returns:
            Dictionary containing all configuration
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML file is malformed
        """
        if self._config is None and self.config_file:
            if not self.config_file.exists():
                raise FileNotFoundError(f"Config file not found: {self.config_file}")
            
            with open(self.config_file, 'r') as f:
                self._config = yaml.safe_load(f)
        
        return self._config or {}
    
    def get_secret(self, key_path: str, default: Any = None) -> Any:
        """
        Get a specific secret value using dot notation.
        
        Args:
            key_path: Dot-separated path to the secret (e.g., 'brightdata.api_key')
            default: Default value if key is not found
            
        Returns:
            The secret value or default
        """
        secrets = self.load_secrets()
        return self._get_nested_value(secrets, key_path, default)
    
    def get_config(self, key_path: str, default: Any = None) -> Any:
        """
        Get a specific config value using dot notation.
        
        Args:
            key_path: Dot-separated path to the config (e.g., 'environment.debug')
            default: Default value if key is not found
            
        Returns:
            The config value or default
        """
        config = self.load_config()
        return self._get_nested_value(config, key_path, default)
    
    def _get_nested_value(self, data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
        """
        Get a nested value from a dictionary using dot notation.
        
        Args:
            data: Dictionary to search in
            key_path: Dot-separated path to the value
            default: Default value if key is not found
            
        Returns:
            The value or default
        """
        keys = key_path.split('.')
        current = data
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def get_brightdata_config(self) -> Dict[str, str]:
        """
        Get BrightData API configuration.
        
        Returns:
            Dictionary with BrightData configuration
        """
        return {
            'api_key': self.get_secret('brightdata.api_key'),
            'dataset_id': self.get_secret('brightdata.dataset_id', 'gd_l7q7dkf244hwjntr0'),
            'base_url': self.get_secret('brightdata.base_url', 'https://api.brightdata.com/datasets')
        }
    
    def get_environment_config(self) -> Dict[str, Any]:
        """
        Get environment configuration.
        
        Returns:
            Dictionary with environment settings
        """
        return {
            'debug': self.get_config('environment.debug', False),
            'log_level': self.get_config('environment.log_level', 'INFO'),
            'max_retries': self.get_config('environment.max_retries', 3),
            'timeout': self.get_config('environment.timeout', 30)
        }
    
    def validate_secrets(self) -> Dict[str, bool]:
        """
        Validate that required secrets are present.
        
        Returns:
            Dictionary indicating which secrets are present
        """
        secrets = self.load_secrets()
        
        required_secrets = {
            'brightdata.api_key': 'BrightData API key',
            'brightdata.dataset_id': 'BrightData dataset ID'
        }
        
        validation = {}
        for key, description in required_secrets.items():
            value = self.get_secret(key)
            validation[description] = value is not None and value != f"your_{key.split('.')[-1]}_here"
        
        return validation


# Global configuration manager instance
config_manager = ConfigManager()


def get_secret(key_path: str, default: Any = None) -> Any:
    """
    Convenience function to get a secret value.
    
    Args:
        key_path: Dot-separated path to the secret
        default: Default value if key is not found
        
    Returns:
        The secret value or default
    """
    return config_manager.get_secret(key_path, default)


def get_config(key_path: str, default: Any = None) -> Any:
    """
    Convenience function to get a config value.
    
    Args:
        key_path: Dot-separated path to the config
        default: Default value if key is not found
        
    Returns:
        The config value or default
    """
    return config_manager.get_config(key_path, default)


def get_brightdata_api_key() -> str:
    """
    Get the BrightData API key.
    
    Returns:
        The API key
        
    Raises:
        ValueError: If API key is not found or not configured
    """
    api_key = get_secret('brightdata.api_key')
    if not api_key or api_key == "your_bright_data_api_key_here":
        raise ValueError(
            "BrightData API key not found. Please set it in secrets.yaml\n"
            "Copy secrets.example.yaml to secrets.yaml and fill in your API key."
        )
    return api_key


def validate_required_secrets() -> None:
    """
    Validate that all required secrets are properly configured.
    
    Raises:
        ValueError: If required secrets are missing
    """
    validation = config_manager.validate_secrets()
    missing = [desc for desc, present in validation.items() if not present]
    
    if missing:
        raise ValueError(
            f"Missing required secrets: {', '.join(missing)}\n"
            f"Please configure them in secrets.yaml"
        )
