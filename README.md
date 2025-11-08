# PySpace – Cross-platform Python Environment Manager

🔍 **Project Summary**

PySpace is a cross-platform CLI tool for managing global Python virtual environments with intelligent caching, daemon support, and automatic synchronization. It provides a seamless way to create, switch between, and manage isolated Python environments across your system.

## Features

- **Environment Management**: Create, list, remove, and switch between virtual environments
- **Intelligent Caching**: Checksum-based package caching for faster installs
- **Daemon Service**: Background daemon for auto-sync and environment monitoring
- **Cross-platform Support**: Works on Windows, macOS, and Linux
- **Pyenv Integration**: Support for multiple Python versions via pyenv
- **Global & Local Configs**: Separate configurations for global and project-specific settings
- **CLI Tooling**: Comprehensive command-line interface with auto-completion

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pyspace.git
   cd pyspace
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install PySpace:
   ```bash
   pip install -e .
   ```

## Usage

### Initialize PySpace in a directory
```bash
pyspace init [env_name]
```

### Create a new environment
```bash
pyspace create my_env --python 3.11
```

### Switch to an environment
```bash
pyspace use my_env
```

### Install packages
```bash
pyspace install numpy pandas
# Or install globally
pyspace install requests --global
```

### List environments
```bash
pyspace list
```

### Remove an environment
```bash
pyspace remove my_env
```

### Show current status
```bash
pyspace status
```

### Clear cache
```bash
pyspace cache-clear
```

### Run diagnostics
```bash
pyspace doctor
```

## Architecture

- `env_manager/`: Core environment management classes (EnvironmentManager, CacheManager, ConfigManager, Utils)
- `daemon/`: Background daemon service with file watching for pyspace.json
- `cli/`: Command-line interface with modular command structure
- `tests/`: Unit and integration tests

Environments are stored in `~/.pyspace/envs/<name>/` with metadata tracking.

## Development

To contribute:

1. Set up development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   python -m pytest tests/
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

## License

MIT License

✨ **Tagline**: "PySpace — Cross-platform Python environment management made simple."