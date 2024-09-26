## Student Console

### Development

1. Install python (https://www.python.org/downloads/)
2. Run `pip install -r requirements-dev.txt`
3. Run `python seed.py`
4. Run `flask --app 'app' --debug run`

#### Before committing:

1. Run `djlint . --reformat`
2. Run `black .`
3. Run unittests: `pytest`

### Using application

#### Logging in:

| Username         | Password | Is Admin |
|------------------|----------|:--------:|
| admin@admin.com  | password |   True   |
| sharia@email.com | password |  False   |

#### Navigation

Use the navigation bar and the on-screen links to browse the website, and perform operations