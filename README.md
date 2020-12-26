## radman

Basic django app to manage icecast stations for private streams.

### Features
- UUID based naming.
- Custom player page.
- Optional stream password protection.
- Configuration file generation for Butt.

### Streaming Tools
- [butt](https://sourceforge.net/projects/butt/) (broadcast using this tool)
- [Android Icecast Broadcast App](https://github.com/faruktoptas/android-icecast-broadcast)

### To Do
- Manage Icecast configuration through Django Admin.

### Development
```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install pipenv
$ pipenv install
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
```

Then add this to `radman/settings/common`:
`SITE_ID = 1`

```bash
$ python3 manage.py runserver
```

### Endpoints
- /admin                    - Django admin.
- /mounts/:uuid             - Mount details (butt / Android broadcast config).


### Run in Production
See docker-compose.yml. Update domains, secrets / passwords in docker-compose.yml and icecast/icecast.xml.

Then run:
```bash
$ docker-compose up -d
```
