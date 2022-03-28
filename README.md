# 291-miniproject-2

Davood 2: electric boogaloo.

## Local Development

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Load JSON

```bash
mkdir mongo_data
mongod --port portNumber --dbpath ./mongo_data &
```

In another terminal,

```bash
python load-json.py
```
