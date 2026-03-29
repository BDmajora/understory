# Understory

Understory is a discovery-first job engine. It finds physical businesses via city registries and resolves their domains to bypass mainstream job board noise.

## Installation

# 1. Create the virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate

# 3. Now install the dependencies inside the venv
pip install -r requirements.txt

# 4. Run the pipeline:
   python3 run.py

## Structure
- run.py: Entry point.
- src/discovery.py: Lethbridge API logic.
- src/resolver.py: Domain resolution logic.
- src/storage.py: JSONL file handling.

## Data
Results are saved to discovery_log.jsonl.