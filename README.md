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
mongod --port 27017 --dbpath ./mongo_data &
```

In another terminal,

```bash
python load-json.py
```

## SSH Stuff on the Server

If i'm working on the lab machines, I'll have to make sure ssh is working.

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_github
```
