
from pathlib import Path

def get_cache_folder():
    pickle_folder = Path.home() / ".cache" / "evdspy"
    return pickle_folder
