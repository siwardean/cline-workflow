"""pytest conftest — adds tests/ to sys.path so helpers can be imported."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
