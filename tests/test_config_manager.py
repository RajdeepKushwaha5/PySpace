from pathlib import Path
from env_manager.config import ConfigManager


def test_config_manager_initialization(tmp_path, monkeypatch):
    """Test config manager initialization."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    cm = ConfigManager()
    assert cm.global_config_file.parent == tmp_path / ".pyspace"


def test_config_get_set(tmp_path, monkeypatch):
    """Test getting and setting config values."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    cm = ConfigManager()

    # Set and get config value
    cm.set("test_key", "test_value")
    assert cm.get("test_key") == "test_value"

    # Get non-existent key with default
    assert cm.get("nonexistent", "default") == "default"
