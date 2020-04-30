## radman

Basic django app to manage stations & mounts of Azuracast for private streams. Supports only IceCast.

### Features
- Mount adding through Azuracast API.
- UUID based naming.
- Custom player page.
- Optional stream password protection.
- Configuration file generation for Butt.

### To Do
- Stations add / remove through API.

### Development
```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install pipenv
$ pipenv install
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
$ python3 manage.py runserver
```

### Endpoints
- /admin                    - Django admin.
- /stations/:uuid           - Station details & mount management on a station.
- /stations/:uuid/add-mount - Add mount.
- /mounts/:uuid             - Mount detais