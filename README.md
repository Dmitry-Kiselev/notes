# notes

## Description ##

Simple notes organizer with authorization and ability to share notes between users.

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



