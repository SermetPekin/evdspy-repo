import os
import shutil
from pathlib import Path  

def clear_cache_folder(cache_folder_path : Path ):
    if 'cache/evdspy' not in str(cache_folder_path) :
        
        print('This does not look like cache folder. I can only delete content of cache folder of evdspy package')
        return 
    if not os.path.exists(cache_folder_path):
        print(f"The folder {cache_folder_path} does not exist.")
        return

    for filename in os.listdir(cache_folder_path):
        file_path = os.path.join(cache_folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    print(f"All files and subdirectories in [{cache_folder_path}] have been deleted.")


def clear_cache():
    from pathlib import Path   
    cache_folder = Path.home() / ".cache" / "evdspy"
    clear_cache_folder(cache_folder)
