# Simple Python API with Falcon

### Prerequisites

Clone the project
```
$ git clone https://github.com/spkenn5/simple-python-api.git gigacover-rest-api
```

This project requires you to have postgres server installed

Please restore the database using the following command.

```
$ psql -f pg_backup.bak postgres
```

Edit `dev.ini` in conf folder accordingly
```
[postgres]
host=localhost
database=simple_python_api
user=postgres
password=postgres
```

Create environment
```
$ virtualenv gigacover
$ source gigacover/bin/activate
```

Install the required packages

```
$ pip install -r install-me.txt
```
### Installation

This project requires Python 3.6.x to run

Install the dependencies and devDependencies and start the server.

```sh
$ cd gigacover-rest-api
$ gunicorn app.main
```

