# tests/conftest.py

import sys
import os

# Определяем корень проекта: папку над tests/ (где лежат src/ и tests/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
