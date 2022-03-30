pyinstaller main.py -F
echo "finished compiling main.py"

pyinstaller load-json.py -F
echo "finished installing load-json.py"

pyinstaller tsv-2-json.py -F
echo "finished installing tsv-2-json.py"


