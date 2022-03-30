rm -rf submit/src
mkdir submit/src

cp util.py submit/src/util.py
cp requirements.txt submit/src/requirements.txt
cp tsv-2-json.py submit/src/
cp load-json.py submit/src/
cp main.py submit/src/

cp dist/load-json submit/dist/load-json
cp dist/main submit/dist/main 
cp dist/tsv-2-json submit/dist/tsv-2-json

mkdir submit/src/commands
cp -r commands/add_cast_crew.py submit/src/commands/add_cast_crew.py
cp -r commands/add_movie.py submit/src/commands/add_movie.py
cp -r commands/search_cast_crew.py submit/src/commands/search_cast_crew.py
cp -r commands/search_genre.py submit/src/commands/search_genre.py
cp -r commands/search_title.py submit/src/commands/search_title.py
