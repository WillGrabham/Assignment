### Student Console

#### Development

1. Install python (https://www.python.org/downloads/)
2. Run `pip install -r requirements-dev.txt`
3. Run `python seed.py`
4. Run `flask --app 'app' run`

Before committing:
1. Run `djlint . --reformat`
2. Run `black .`