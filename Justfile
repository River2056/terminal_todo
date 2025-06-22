run:
    python main.py

dev:
    textual run --dev main.py

console:
    textual console

activate:
    source ./.venv/bin/activate

package:
    pyinstaller --onefile main.py --name todos
