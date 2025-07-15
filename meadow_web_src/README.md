# Meadow Web Server

## What's This?

This folder contains the web server for the Meadow Bitcoin Node. It gives you a browser-based interface and some handy API endpoints so you can actually interact with the node — no need to live in the terminal (unless you want to, of course).

## What's in the Box?

Here's a quick rundown of the files and folders:

- `app.py` — Kicks things off and wires up the whole Flask app
- `bitcoin_utils.py` — Bitcoin-related helper stuff lives here
- `config.py` — Settings and config options
- `extensions.py` — Flask extension setup (because boilerplate happens)
- `models.py` — App data models (not the AI kind)
- `routes/` — All the API routes are here
- `static/` — Your CSS, JavaScript, images, etc.
- `templates/` — HTML templates for the web UI
- `utils/` — Random useful things that didn’t fit elsewhere

## Dependencies

Everything you need is listed in `requirements.txt`.

This server is meant to be bundled inside the full Meadow system via Buildroot. But if you’re just poking around or doing some dev work locally, you can run it standalone.

## Getting It Running (Dev Mode)

1. Make a virtual environment: `python -m venv .venv`
2. Activate it and install the goods: `pip install -r requirements.txt`
3. Run it: `python app.py`

Boom. You’ve got a web server.

## What It Can Do

Once it’s up and running, the web UI lets you:
- See what your node is up to
- Tweak node settings
- Peek into the blockchain
- Manage operations without SSHing into your Pi like it’s 2013

## Integration Notes

This thing talks directly to the Bitcoin node running in the background and wraps it all in a friendly interface so you (or your less techy friends) can use it without needing a CLI cheat sheet.

More features will probably sneak in over time — PRs and ideas are welcome.
