import json
from pathlib import Path
from typing import Dict, Any
from loguru import logger


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".pyspace"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.global_config_file = self.config_dir / "config.json"
        self._load_config()

    def _load_config(self):
        if self.global_config_file.exists():
            with open(self.global_config_file) as f:
                self.config = json.load(f)
        else:
            self.config = {
                "python_version": "3.11",
                "default_env": None,
                "auto_sync": True,
            }
            self._save_config()

    def _save_config(self):
        with open(self.global_config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self._save_config()

    def get_local_config(self) -> Dict:
        """Get local pyspace.json config."""
        local_config = Path.cwd() / "pyspace.json"
        if local_config.exists():
            with open(local_config) as f:
                return json.load(f)
        return {}

    def set_local_config(self, config: Dict):
        """Set local pyspace.json config."""
        logger.info(f"Setting local config: {config}")
        try:
            local_config = Path.cwd() / "pyspace.json"
            with open(local_config, "w") as f:
                json.dump(config, f, indent=2)
            logger.success("Local config saved successfully")
        except Exception as e:
            logger.error(f"Failed to save local config: {e}")
