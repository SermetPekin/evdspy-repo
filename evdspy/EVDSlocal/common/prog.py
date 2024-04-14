from rich import print
import time
from rich.progress import track

def rich_sim(num , msg ):
    for i in track(range(num), description=msg):
        time.sleep(1)