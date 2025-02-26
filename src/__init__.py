from .globals import *
from pathlib import Path 
import json

if not Path(DATABASE).exists():
    with open(DATABASE, "w") as f:
        json.dump({}, f)
