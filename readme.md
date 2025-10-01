# Setup Guide

## Clone the repo

```
git clone <https url>
```

## Move inside the directory
```
cd <repo name>
```

### Create a virtual environment
```
python3 -m venv env
```

### Activate the virtual environment

* macOS/Linux:
    ```
    source env/bin/activate
    ```
* Windows:

    ```
    env\Scripts\activate
    ```

## Install the required packages

* command: 
    ```
    pip install -r requirement.txt
    ```

## Copy sample.env to .env
```
cp sample.env .env
```

> Note: Replace the keys with the variable value as you want and setup your database and put replace with the name host and database name

## Migrations

### Initialize the alembic
```
alembic init migrations
```

### After successfully initialization  change into the alembic.ini file

```
sqlalchemy.url = <here your database url which you mention in the .env file >
```

### Generate the migrations files
```
alembic revision --autogenerate 
```
### Apply the migrations

```
alembic upgrade head
```

## Run the Project

```
uvicorn main:app --reload
```