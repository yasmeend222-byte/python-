"""
Configuration management for AI Safe Guardian System
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from .exceptions import ConfigurationError


class Config:
    """Manages configuration loading and access"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to YAML config file. If None, uses default.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config: Dict[str, Any] = {}
        self.load()
    
    @staticmethod
    def _get_default_config_path() -> str:
        """Get default configuration path"""
        base_dir = Path(__file__).parent.parent
        default_config = base_dir / "config" / "default.yaml"
        
        if not default_config.exists():
            raise ConfigurationError(
                f"Default config not found at {default_config}"
            )
        
        return str(default_config)
    
    def load(self) -> None:
        """Load configuration from YAML file"""
        if not Path(self.config_path).exists():
            raise ConfigurationError(
                f"Configuration file not found: {self.config_path}"
            )
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML configuration: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
        
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration structure"""
        required_sections = ['safety', 'modules']
        
        for section in required_sections:
            if section not in self.config:
                raise ConfigurationError(f"Missing required config section: {section}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'safety.enabled' or 'modules.rate_limiter.enabled')
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation
        
        Args:
            key: Configuration key (e.g., 'safety.enabled')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def is_enabled(self, module: str) -> bool:
        """Check if a module is enabled"""
        return self.get(f'modules.{module}.enabled', False)
    
    def get_module_config(self, module: str) -> Dict[str, Any]:
        """Get configuration for a specific module"""
        return self.get(f'modules.{module}', {})
    
    def reload(self) -> None:
        """Reload configuration from file"""
        self.load()
    
    def to_dict(self) -> Dict[str, Any]:
        """Get entire configuration as dictionary"""
        return self.config.copy()


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """
    Get or create global configuration instance
    
    Args:
        config_path: Path to config file (only used on first call)
    
    Returns:
        Config instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config(config_path)
    
    return _config_instance
