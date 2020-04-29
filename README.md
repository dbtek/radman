## radman

Basic django app to manage stations & mounts of Azuracast for private streams.

### Features
- UUID based naming.
- Custom player page.

### To Do
- Stations add / remove through API.
- Stream password protection.

### Development
```bash
$ python3 -m venv .venv
$ pip install pipenv
$ pipenv install
$ python3 manage.py runserver
```

### Endpoints

- /stations/:uuid           - Station details & mount management on a station.
- /stations/:uuid/add-mount - Add mount.
- /mounts/:uuid             - Mount detais