## Backend Version Demo

https://user-images.githubusercontent.com/7946260/122238076-d7226c00-ce8d-11eb-9602-b9d897120e19.mov

## Frontend Version Demo

https://user-images.githubusercontent.com/7946260/122238032-ceca3100-ce8d-11eb-91f2-98454ff1137f.mov

### Running tests

```
yarn autoflake
yarn pytest:fresh
```

Or check out `package.json` for other options.

### Server architecture

- PostgreSQL 10+
- Python 3.9+
- Django 3
- [django-environ](https://github.com/joke2k/django-environ) for easy environment configuration via `.env` files

