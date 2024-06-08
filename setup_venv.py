import os
import subprocess
import sys
from pathlib import Path

# Add to __init__.py: from . import setup_venv

venv_path = Path(__file__).parent / '.venv'
main_venv_path = (Path(__file__).parent / '../../.venv').resolve()

if not (venv_path / ('Scripts' if os.name == 'nt' else 'bin') / 'activate').exists():
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', str(venv_path)])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create virtual environment: {e}")
    
    requirements_file = Path(__file__).parent / 'requirements.txt'
    if requirements_file.exists():
        bin_path = venv_path / ('Scripts' if os.name == 'nt' else 'bin') / ('pip.exe' if os.name == 'nt' else 'pip')
        
        if not bin_path.exists():
            raise FileNotFoundError(f"pip not found at {bin_path}")
        
        try:
            subprocess.check_call([str(bin_path), 'install', '-r', str(requirements_file)])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install requirements: {e}")

site_packages = venv_path / 'lib' / 'site-packages'
if os.name != 'nt':  # Adjust for Unix-like OS site-packages location
    site_packages = venv_path / 'lib' / f'python{sys.version_info.major}.{sys.version_info.minor}' / 'site-packages'

if str(site_packages) not in sys.path:
    sys.path.insert(0, str(site_packages))
