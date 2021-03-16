#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Draughts adaptation of web-boardimage by Niklas Fiekas <niklas.fiekas@backscattering.de>.
# Distributed under the same license:
#
# web-boardimage is an HTTP service that renders chess board images.
# Copyright (C) 2016-2017 Niklas Fiekas <niklas.fiekas@backscattering.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""An HTTP service that renders draughts board images"""

import argparse
import asyncio
import aiohttp.web
import draughts
import draughts_svg
import cairosvg
import re
from urllib.parse import unquote


class Service:
    def __init__(self, css=None):
        self.css = css

    def make_svg(self, request):
        try:
            board_size = int(request.query.get("boardSize") or request.query.get("boardsize", 10))
            if board_size % 2 != 0 or board_size < 2:
                raise ValueError("boardsize is not even or too small")
        except ValueError:
            raise aiohttp.web.HTTPBadRequest(reason="invalid boardsize")

        try:
            parts = unquote(request.query["fen"]).split(":")
            board = draughts.BaseBoard(":".join(parts[:3]), board_size)
        except KeyError:
            raise aiohttp.web.HTTPBadRequest(reason="fen required")
        except ValueError:
            raise aiohttp.web.HTTPBadRequest(reason="invalid fen")

        try:
            size = min(max(int(request.query.get("size", 360)), 16), 1024)
        except ValueError:
            raise aiohttp.web.HTTPBadRequest(reason="size is not a number")

        try:
            uci = request.query.get("lastMove") or request.query["lastmove"]
            lastmove = uci
        except KeyError:
            lastmove = None
        except ValueError:
            raise aiohttp.web.HTTPBadRequest(reason="lastMove is not a valid move")

        try:
            arrows = [arrow(s.strip()) for s in unquote(request.query.get("arrows", "")).split(",") if s.strip()]
        except ValueError:
            raise aiohttp.web.HTTPBadRequest(reason="invalid arrow")

        flipped = request.query.get("orientation", "white") == "black"

        return draughts_svg.board(board, flipped=flipped, lastmove=lastmove, arrows=arrows, size=size, style=self.css)

    @asyncio.coroutine
    def render_svg(self, request):
        return aiohttp.web.Response(text=self.make_svg(request), content_type="image/svg+xml")

    @asyncio.coroutine
    def render_png(self, request):
        svg_data = self.make_svg(request)
        png_data = cairosvg.svg2png(bytestring=svg_data)
        return aiohttp.web.Response(body=png_data, content_type="image/png")


def arrow(s):
    tail = int(s[:2])
    head = int(s[2:]) if len(s) > 2 else tail
    return draughts_svg.Arrow(tail, head)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", "-p", type=int, default=8080, help="web server port")
    parser.add_argument("--bind", default="127.0.0.1", help="bind address (default: 127.0.0.1)")
    parser.add_argument("--css", type=argparse.FileType("r"))
    args = parser.parse_args()

    app = aiohttp.web.Application()
    service = Service(args.css.read() if args.css else None)
    app.router.add_get("/board.png", service.render_png)
    app.router.add_get("/board.svg", service.render_svg)

    aiohttp.web.run_app(app, port=args.port, host=args.bind, access_log=None)
