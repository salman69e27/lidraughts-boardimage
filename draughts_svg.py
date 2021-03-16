# -*- coding: utf-8 -*-
#
# Minimal implementation for draughts of the python-chess library by Niklas Fiekas <niklas.fiekas@backscattering.de>.
# Distributed under the same license:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import draughts
import collections
import math

import xml.etree.ElementTree as ET


SQUARE_SIZE = 45

PIECES = {
    "M": """<g id="white-man" class="white man" viewBox="0 0 210 210"><defs><linearGradient id="lgw1"><stop style="stop-color: #7f7f7f; stop-opacity: 1;" offset="0"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgw1); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><path d="M 10,105 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0 z" style="fill: rgb(255, 255, 255); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/></g>""",
    "K": """<g id="white-king" class="white king" viewBox="0 0 210 210"><defs><linearGradient id="lgw2"><stop style="stop-color: #7f7f7f; stop-opacity: 1;" offset="0"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgw2); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><path d="M 10,105 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgw2) rgb(255, 255, 255); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><path d="M 10,70 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0 z" style="fill: rgb(255, 255, 255); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><polygon points="58,45  71,85 139,85  152,45  127,70 105,35 83,70" fill="#bf8c16"/><polygon points="74,96 71.6,87  138.4,87 136,96" fill="#bf8c16"/><ellipse fill="#FFFFFF" cx="105" cy="68" rx="5" ry="10"/></g>""",
    "G": """<g id="white-ghostman" class="white ghostman" viewBox="0 0 210 210" opacity="0.3"><defs><linearGradient id="lgw3"><stop style="stop-color: #7f7f7f; stop-opacity: 1;" offset="0"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgw3); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><path d="M 10,105 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0 z" style="fill: rgb(255, 255, 255); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/></g>""",
    "P": """<g id="white-ghostking" class="white ghostking" viewBox="0 0 210 210" opacity="0.3"><defs><linearGradient id="lgw4"><stop style="stop-color: #7f7f7f; stop-opacity: 1;" offset="0"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #ffffff; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgw4); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><path d="M 10,105 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgw4) rgb(255, 255, 255); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><path d="M 10,70 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0 z" style="fill: rgb(255, 255, 255); stroke: rgb(0, 0, 0); stroke-width: 3; stroke-opacity: 0.65;"/><polygon points="58,45  71,85 139,85  152,45  127,70 105,35 83,70" fill="#bf8c16"/><polygon points="74,96 71.6,87  138.4,87 136,96" fill="#bf8c16"/><ellipse fill="#FFFFFF" cx="105" cy="68" rx="5" ry="10"/></g>""",
    "m": """<g id="black-man" class="black man" viewBox="0 0 210 210"><defs><linearGradient id="lgb1"><stop style="stop-color: #000000; stop-opacity: 1;" offset="0"/><stop style="stop-color: #000000; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #9f9f9f; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgb1); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><path d="M 10,105 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0" style="fill: rgb(0, 0, 0); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/></g>""",
    "k": """<g id="black-king" class="black king" viewBox="0 0 210 210"><defs><linearGradient id="lgb2"><stop style="stop-color: #000000; stop-opacity: 1;" offset="0"/><stop style="stop-color: #000000; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #9f9f9f; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgb2); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><path d="M 10,105 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgb2) rgb(0, 0, 0); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><path d="M 10,70 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0 z" style="fill: rgb(0, 0, 0); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><polygon points="58,45  71,85 139,85  152,45  127,70 105,35 83,70" fill="#bf8c16"/><polygon points="74,96 71.6,87  138.4,87 136,96" fill="#bf8c16"/><ellipse fill="#000000" cx="105" cy="68" rx="5" ry="10"/></g>""",
    "g": """<g id="black-ghostman" class="black ghostman" viewBox="0 0 210 210" opacity="0.3"><defs><linearGradient id="lgb3"><stop style="stop-color: #000000; stop-opacity: 1;" offset="0"/><stop style="stop-color: #000000; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #9f9f9f; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgb3); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><path d="M 10,105 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0" style="fill: rgb(0, 0, 0); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/></g>""",
    "p": """<g id="black-ghostking" class="black ghostking" viewBox="0 0 210 210" opacity="0.3"><defs><linearGradient id="lgb4"><stop style="stop-color: #000000; stop-opacity: 1;" offset="0"/><stop style="stop-color: #000000; stop-opacity: 1;" offset="0.5"/><stop style="stop-color: #9f9f9f; stop-opacity: 1;" offset="1"/></linearGradient></defs><path d="M 10,140 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgb4); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><path d="M 10,105 c 0,60 190,60 190,0 l 0,-35 l -190,0 z" style="fill: url(#lgb4) rgb(0, 0, 0); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><path d="M 10,70 c 0,60 190,60 190,0 c 0,-60 -190,-60 -190,0 z" style="fill: rgb(0, 0, 0); stroke: #dfdfdf; stroke-width: 3; stroke-opacity: 0.5;"/><polygon points="58,45  71,85 139,85  152,45  127,70 105,35 83,70" fill="#bf8c16"/><polygon points="74,96 71.6,87  138.4,87 136,96" fill="#bf8c16"/><ellipse fill="#000000" cx="105" cy="68" rx="5" ry="10"/></g>"""
}

DEFAULT_COLORS = {
    "square light": "#ffce9e",
    "square dark": "#d18b47",
    "square dark lastmove": "#aaa23b",
    "square light lastmove": "#cdd16a",
}


class Arrow(collections.namedtuple("Arrow", "tail head")):
    """Details of an arrow to be drawn."""

    __slots__ = ()


class SvgWrapper(str):
    def _repr_svg_(self):
        return self


def _svg(viewbox, size):
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "version": "1.1",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "viewBox": "0 0 %d %d" % (viewbox, viewbox),
    })

    if size is not None:
        svg.set("width", str(size))
        svg.set("height", str(size))

    return svg


def _text(content, x, y, width, height):
    t = ET.Element("text", {
        "x": str(x + width // 2),
        "y": str(y + height // 2),
        "font-size": str(max(1, int(min(width, height) * 0.7))),
        "text-anchor": "middle",
        "alignment-baseline": "middle",
    })
    t.text = content
    return t


def piece(piece, size=None):
    """
    Renders the given :class:`draughts.Piece` as an SVG image.
    """
    svg = _svg(SQUARE_SIZE, size)
    svg.append(ET.fromstring(PIECES[piece.symbol()]))
    return SvgWrapper(ET.tostring(svg).decode("utf-8"))


def board(board=None, *, flipped=False, lastmove=None, arrows=(), size=None, style=None):
    """
    Renders a board with pieces and/or arrows as an SVG image.
    :param board: A :class:`draughts.BaseBoard` for a draughtsboard with pieces or
        ``None`` (the default) for a draughtsboard without pieces.
    :param flipped: Pass ``True`` to flip the board.
    :param lastmove: An uci sequence to be highlighted.
    :param arrows: A list of :class:`~draughts.svg.Arrow` objects or a list of tuples
        . An arrow from a square pointing to the same square is drawn as a circle
    :param size: The size of the image in pixels (e.g., ``400`` for a 400 by
        400 board) or ``None`` (the default) for no size limit.
    :param style: A CSS stylesheet to include in the SVG image.
    """
    board_size = board.board_size if board else 10
    margin = 0
    svg = _svg(board_size * SQUARE_SIZE + 2 * margin, size)

    if style:
        ET.SubElement(svg, "style").text = style

    if lastmove:
        uciparts = [int(lastmove[i:i+2]) for i in range(0, len(lastmove), 2)]

    defs = ET.SubElement(svg, "defs")
    if board:
        for color in draughts.COLORS:
            for piece_type in draughts.PIECE_TYPES:
                if board.contains_piece(piece_type, color):
                    defs.append(ET.fromstring(PIECES[draughts.Piece(piece_type, color).symbol()]))

    for square in range(board_size ** 2):

        x_index = square % board_size
        y_index = int((square + (board_size - x_index)) / board_size - 1)
        x = (x_index if not flipped else board_size - 1 - x_index) * SQUARE_SIZE + margin
        y = (y_index if not flipped else board_size - 1 - y_index) * SQUARE_SIZE + margin

        square_uci = int(square / 2) + 1 if x_index % 2 != y_index % 2 else -1

        cls = ["square", "light" if x_index % 2 == y_index % 2 else "dark"]
        if lastmove and square_uci != -1 and square_uci in uciparts:
            cls.append("lastmove")
        fill_color = DEFAULT_COLORS[" ".join(cls)]

        ET.SubElement(svg, "rect", {
            "x": str(x),
            "y": str(y),
            "width": str(SQUARE_SIZE),
            "height": str(SQUARE_SIZE),
            "class": " ".join(cls),
            "stroke": "none",
            "fill": fill_color,
        })

        # Render pieces.
        if square_uci != -1 and board is not None:
            piece = board.piece_at(square_uci)
            if piece:
                ET.SubElement(svg, "use", {
                    "xlink:href": "#%s-%s" % (draughts.COLOR_NAMES[piece.color], draughts.PIECE_NAMES[piece.piece_type]),
                    "transform": "translate(%d, %d) scale(%f, %f)" % (x, y, SQUARE_SIZE / 210, SQUARE_SIZE / 210),
                })

    for tail, head in arrows:

        tail_conv = tail * 2 - 1
        tail_y = (tail_conv + (board_size - tail_conv % board_size)) / board_size - 1
        tail_x = tail_conv % board_size - tail_y % 2

        head_conv = head * 2 - 1
        head_y = (head_conv + (board_size - head_conv % board_size)) / board_size - 1
        head_x = head_conv % board_size - head_y % 2

        xtail = margin + (tail_x + 0.5 if not flipped else board_size - 0.5 - tail_x) * SQUARE_SIZE
        ytail = margin + (board_size - 0.5 - tail_y if flipped else tail_y + 0.5) * SQUARE_SIZE

        xhead = margin + (head_x + 0.5 if not flipped else board_size - 0.5 - head_x) * SQUARE_SIZE
        yhead = margin + (board_size - 0.5 - head_y if flipped else head_y + 0.5) * SQUARE_SIZE

        if (head_x, head_y) == (tail_x, tail_y):
            ET.SubElement(svg, "circle", {
                "cx": str(xhead),
                "cy": str(yhead),
                "r": str(SQUARE_SIZE * 0.9 / 2),
                "stroke-width": str(SQUARE_SIZE * 0.1),
                "stroke": "#888",
                "fill": "none",
                "opacity": "0.5",
            })
        else:
            marker_size = 0.75 * SQUARE_SIZE
            marker_margin = 0.1 * SQUARE_SIZE

            dx, dy = xhead - xtail, yhead - ytail
            hypot = math.hypot(dx, dy)

            shaft_x = xhead - dx * (marker_size + marker_margin) / hypot
            shaft_y = yhead - dy * (marker_size + marker_margin) / hypot

            xtip = xhead - dx * marker_margin / hypot
            ytip = yhead - dy * marker_margin / hypot

            ET.SubElement(svg, "line", {
                "x1": str(xtail),
                "y1": str(ytail),
                "x2": str(shaft_x),
                "y2": str(shaft_y),
                "stroke": "#888",
                "stroke-width": str(SQUARE_SIZE * 0.2),
                "opacity": "0.5",
                "stroke-linecap": "butt",
                "class": "arrow",
            })

            marker = [(xtip, ytip),
                      (shaft_x + dy * 0.5 * marker_size / hypot,
                       shaft_y - dx * 0.5 * marker_size / hypot),
                      (shaft_x - dy * 0.5 * marker_size / hypot,
                       shaft_y + dx * 0.5 * marker_size / hypot)]

            ET.SubElement(svg, "polygon", {
                "points": " ".join(str(x) + "," + str(y) for x, y in marker),
                "fill": "#888",
                "opacity": "0.5",
                "class": "arrow",
            })

    return SvgWrapper(ET.tostring(svg).decode("utf-8"))