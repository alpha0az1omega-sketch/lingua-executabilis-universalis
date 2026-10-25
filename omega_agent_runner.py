# Ce script est lancé automatiquement par GitHub Actions
# Il génère 10 nouvelles entités et met à jour la base de données.
import sys
import os
sys.path.append(os.path.abspath('02_MVP'))
from genesis_engine import run_genesis_cycle

if __name__ == "__main__":
    run_genesis_cycle()
