import sys
import os
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)
from infrastructure.presentation.api import run_api

if __name__ == "__main__":
    run_api()

