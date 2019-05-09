# Simple Python API with Falcon

### Prerequisites
This project requires you to have postgres server installed

Please restore the database using the following command.

```
$ psql -f pg_backup.bak postgres
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
$ git clone https://github.com/spkenn5/simple-python-api.git gigacover-rest-api
$ cd gigacover-rest-api
$ gunicorn app.main
```

