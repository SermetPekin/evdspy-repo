import os
import traceback

# from dotenv import load_dotenv
from pathlib import Path

try:

    from dotenv import load_dotenv


    def load_env(verbose=False):
        """Load environment variables from a .env file in the current directory."""
        dotenv_path = Path(".") / '.env'
        if verbose:
            print(f"reading apikey from [{dotenv_path}]")
        load_dotenv(dotenv_path)

except Exception:

    print("""[solution]
          $ pip install python-dotenv 
          """)
    traceback.print_exc()

    raise ModuleNotFoundError()
