## Backend Version Demo

https://user-images.githubusercontent.com/7946260/122238076-d7226c00-ce8d-11eb-9602-b9d897120e19.mov

## Backend Description

1. Assuming a standard deck (52 cards of 4 suits: ♣ Clubs, ♦ Diamonds, ♥ Hearts, ♠ Spades).
2. Press a "Deal" button to deal 5 random cards.
   - Make this a mutation
3. Pressing the button again should deal 5 unique, random cards. Within the same game, you should never get the same cards again that you got in the past (just like a physical deck).
   - Same mutation.
   - For storing data/state, any clean solution goes if you wanna focus on other parts.
4. API for a card counter which shows how many cards are dealt/left.
5. API to reset the game.
6. API to show the game is over.
7. API for win/lose. If there is an ace in the last draw, display You Win, otherwise display You Lose, Sucker.
8. Unit tests.

You can run a sample query at http://localhost:5000/graphql/

```graphql
query {
  me {
    username
    email
  }
}
```

### Getting started

On MacOS, use [brew](https://brew.sh/) to manage installation of supporting programs, as it keeps things tidy.

For backend, the recommended way is to use poetry and pyenv. All of the commands in this section are from the `server` folder.

You may also work in docker, using the provided `./docker-assist` and `docker-compose.yml`, but it's generally quicker to develop locally. See `docker/Docker.server/Dockerfile` for the docker setup, and note that poetry is set up to export to `requirements.txt`.

Install [poetry](https://python-poetry.org/). To manage python versions, we recommend installing [`pyenv`](https://github.com/pyenv/pyenv). See [the `poetry` documentation](https://python-poetry.org/docs/managing-environments/) for details.

Then install Python dependencies:

    cd server/
    # try one of these
    pyenv install 3.9.5  # or pyenv local 3.9.5
    poetry env use ~/.pyenv/versions/3.9.5/bin/python
    poetry install
    # or
    poetry install --python `which python3`

If you don't have it already, you'll also want to install Postgres. Version 10 or later should be fine.

If you have issues:

- Check which pyenv version homebrew installs https://github.com/Homebrew/homebrew-core/blob/master/Formula/pyenv.rb#L4
- See what versions of python that pyenv version supports: https://github.com/pyenv/pyenv/tree/v1.2.19/plugins/python-build/share/python-build

Copy example env vars to `.env`. You might need to change `DATABASE_URL` based on your environment.

    cp ../.env.example ../.env

Create the `cardgame` database:

    createdb cardgame

Load the sample user data:

    poetry run ./manage.py migrate
    poetry run ./manage.py loaddata cardgame/fixtures/users.json
    poetry run ./manage.py runserver 5000

Now you can go to http://localhost:5000, http://localhost:5000/graphql/, or http://localhost:5000/admin/ for the Django admin.

### Installing packages

```
poetry add <package name>  # this automatically adds it to pyproject.toml and poetry.lock
```

If you manually update `pyproject.toml`, make sure you run `poetry update` to update the lockfile.

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

