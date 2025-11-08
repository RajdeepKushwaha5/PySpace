import json
from pathlib import Path

DEFAULT_CONFIG = {
    "python_version": "3.11",
    "default_cache_path": "~/.pyspace/cache/wheels",
    "workspace_root": "~/.pyspace/workspaces",
    "daemon_port": 5132,
    "use_uv": False,
}


class ConfigManager:
    def __init__(self):
        self.config_path = Path.home() / ".pyspace" / "config.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self.config = DEFAULT_CONFIG.copy()
            self.save()
        else:
            with open(self.config_path) as f:
                self.config = json.load(f)
            # Merge with defaults for missing keys
            for key, value in DEFAULT_CONFIG.items():
                if key not in self.config:
                    self.config[key] = value
            self.save()

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        self.save()
