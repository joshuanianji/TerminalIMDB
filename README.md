# 291-miniproject-2

Davood 2: electric boogaloo.

## Local Development

```bash
python -m env venv 
source venv/bin/activate
pip install -r requirements.txt
```

### Load JSON

```bash
mkdir mongo_data
mongod --port 27017 --dbpath ./mongo_data &
```

In another terminal,

```bash
python load_json.py
```