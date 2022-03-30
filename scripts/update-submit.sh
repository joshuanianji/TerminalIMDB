mkdir submit 
mkdir submit/src

rm -rf submit/src
mkdir submit/src

cp util.py submit/src/util.py
cp requirements.txt submit/src/requirements.txt
cp tsv-2-json.py submit/src/
cp load-json.py submit/src/
cp main.py submit/src/
cp -r dist submit/dist
cp -r commands submit/src/commands

