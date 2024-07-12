# Ludoist
Multiplayer Ludo game written in Python.

Ludoist is written using Pyglet and uses sockets for multiplayer Ludo matches for 2 to 4 players.

:warning: This project is currently in development.

## Installation
Ludoist requires at least Python 3.8 or a higher version.

Clone this repository and install dependencies:

```
$ git clone https://github.com/izxxr/ludoist
$ cd ludoist
$ pip install -r requirements.txt
```

The server has to be started:

```
$ python start_server.py
```

To change the host and port the server runs on, see `server_config.json`. By default, it runs on localhost and port 4590.

Client can be started by running the `start_client.py` file but must be ran when server is running.