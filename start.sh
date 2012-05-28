hash python2 2>/dev/null || {
	echo "PyMCServer requires Python 2.x to run."
	exit 1
}

DIR="$(dirname "$0")"
cd "$DIR"

export PYTHONPATH="$PYTHONPATH:src"
python2 src/pymcserver/main.py
