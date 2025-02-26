from .globals import *
from pathlib import Path 
import json

if not Path(DATABASE).exists():
    if not Path(DATABASE).parent.exists():
        Path(DATABASE).parent.mkdir(parents=True)

    with open(DATABASE, "w") as f:
        json.dump({}, f)
