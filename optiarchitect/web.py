"""Launcher for the browser interface:  ``optiarchitect-web``  (needs ``pip install optiarchitect[web]``)."""
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print("The web interface needs Streamlit:  pip install \"optiarchitect[web]\"", file=sys.stderr)
        return 1
    app = Path(__file__).with_name("app.py")
    return subprocess.call([sys.executable, "-m", "streamlit", "run", str(app), *sys.argv[1:]])


if __name__ == "__main__":
    sys.exit(main())
