lidraughts-boardimage
==============

An HTTP service that renders draughts board images, used for [lidraughts.org](https://lidraughts.org)

It includes a minimal implementation of the [python-chess](https://github.com/niklasf/python-chess) library for draughts (only piece/board representation and svg).

It uses the same API as [web-boardimage](https://github.com/niklasf/web-boardimage), where move notation and FEN strings are replaced by their draughts counterparts. See the adapted installation and usage instructions below.

Usage
-----

```
python3 server.py [--port 8080] [--bind 127.0.0.1] [--css default.css]
```

Installation
------------

Requires Python 3.4+.

```
sudo apt-get install python3-dev libffi-dev libxml2-dev libxslt1-dev libcairo2

pip install -r requirements.txt
```

HTTP API
--------

### `GET /board.svg` render an SVG

name | type | default | description
--- | --- | --- | ---
**fen** | string | required | FEN of the position with at least the board part
**orientation** | string | white | `white` or `black`
**size** | int | 360 | The width and height of the image
**lastMove** | string | *(none)* | The last move to highlight, e.g. `0510`
**arrows** | string | *(none)* | Draw arrows and circles, e.g. `0622,44`

### `GET /board.png` render a PNG
