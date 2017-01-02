# notes

## Installation ##

### Install python dependencies ###

```bash
python install -r requirement.txt
```

### Install frontend libraries and frameworks ###

```bash
# open console in static directory
cd notes/authorization/static

# install dependencies with bower
bower install
```

### Create  tables in the database ###

```bash
python manage.py makemigrations note
python manage.py migrate
```


## Demo ##
http://dmitrykiselev.pythonanywhere.com/


## Known issues ##
<ul>
    <li>[authorization] if the user enters weak password - wrong error message displays (password_mismatch).</li>
</ul>
