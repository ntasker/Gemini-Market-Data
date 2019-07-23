A virtual enviroment [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) can be used to run this program

```bash
# Create a virtualenv in which we can install the dependencies
python3 -m venv env
source env/bin/activate
```

Now we can install our dependencies:

```bash
pip install -r requirements.txt
```

Run the program with:

```bash
python manage.py runserver
```
