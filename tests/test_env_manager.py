from unittest.mock import patch
from env_manager.environment import EnvironmentManager


@patch("env_manager.utils.run_command")
def test_create_environment(mock_run, tmp_path):
    """Test creating a virtual environment."""
    # Mock venv creation success
    mock_run.return_value = (0, "", "")

    env_manager = EnvironmentManager(base_dir=tmp_path / "envs")
    result = env_manager.create_environment("test_env")
    assert result is True

    # Verify environment was created
    envs = env_manager.list_environments()
    assert len(envs) == 1
    assert envs[0]["name"] == "test_env"


def test_environment_already_exists(tmp_path):
    """Test creating environment that already exists."""
    env_manager = EnvironmentManager(base_dir=tmp_path / "envs")

    # Create a directory to simulate existing environment
    (tmp_path / "envs" / "test_env").mkdir(parents=True)

    # Try to create same environment again
    result = env_manager.create_environment("test_env")
    assert result is False


@patch("env_manager.utils.run_command")
def test_remove_environment(mock_run, tmp_path):
    """Test removing an environment."""
    # Mock venv creation success
    mock_run.return_value = (0, "", "")

    env_manager = EnvironmentManager(base_dir=tmp_path / "envs")
    env_manager.create_environment("test_env")

    # Remove environment
    result = env_manager.remove_environment("test_env")
    assert result is True

    # Verify it was removed
    envs = env_manager.list_environments()
    assert len(envs) == 0
