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

# Piece vector graphics are copyright (C) Colin M.L. Burnett
# <https://en.wikipedia.org/wiki/User:Cburnett> and also licensed under the
# GNU General Public License.

COLORS = [WHITE, BLACK] = [True, False]
COLOR_NAMES = ["black", "white"]

PIECE_TYPES = [MAN, KING, GHOSTMAN, GHOSTKING] = range(1, 5)
PIECE_SYMBOLS = [None, "m", "k", "g", "p"]
PIECE_NAMES = [None, "man", "king", "ghostman", "ghostking"]

STARTING_BOARD_FEN = "W:W31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50:B1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20"

class Piece:
    """A piece with type and color."""

    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color

    def symbol(self):
        """
        Gets the symbol ``M``, ``K``, ``G`` or ``P`` for white
        pieces or the lower-case variants for the black pieces.
        """
        if self.color == WHITE:
            return PIECE_SYMBOLS[self.piece_type].upper()
        else:
            return PIECE_SYMBOLS[self.piece_type]

    def __hash__(self):
        return hash(self.piece_type * (self.color + 1))

    def __repr__(self):
        return "Piece.from_symbol('{}')".format(self.symbol())

    def __str__(self):
        return self.symbol()

    def _repr_svg_(self):
        import draughts.svg
        return draughts.svg.piece(self, size=45)

    def __eq__(self, other):
        ne = self.__ne__(other)
        return NotImplemented if ne is NotImplemented else not ne

    def __ne__(self, other):
        try:
            if self.piece_type != other.piece_type:
                return True
            elif self.color != other.color:
                return True
            else:
                return False
        except AttributeError:
            return NotImplemented

    @classmethod
    def from_symbol(cls, symbol):
        """
        Creates a :class:`~draughts.Piece` instance from a piece symbol.
        :raises: :exc:`ValueError` if the symbol is invalid.
        """
        if symbol.islower():
            return cls(PIECE_SYMBOLS.index(symbol), BLACK)
        else:
            return cls(PIECE_SYMBOLS.index(symbol.lower()), WHITE)


class BaseBoard:
    """
    A board representing the position of draughts pieces.
    The board is initialized with the standard draughts starting position, unless
    otherwise specified in the optional *board_fen* argument. If *board_fen*
    is ``None``, an empty board is created.
    The *board_size* argument sets the amount of squares for the width and height
    of the board.
    :raises: :exc:`ValueError` if the board size is invalid.
    """
    def __init__(self, board_fen=STARTING_BOARD_FEN, board_size=10):
        self.board_size = board_size
        if self.board_size % 2 != 0 or self.board_size < 2:
            raise ValueError("invalid board_size: {}".format(board_size))
        if board_fen is None:
            self._clear_board()
        elif board_fen == STARTING_BOARD_FEN:
            self._reset_board()
        else:
            self._set_board_fen(board_fen)

    def _reset_board(self):
        self.pieces = {}
        fields = self.board_size ** 2 // 2
        piece_count = (self.board_size // 2 - 1) * (self.board_size // 2)
        for b in range(1, piece_count + 1):
            self.pieces[b] = Piece.from_symbol("m")
        for w in range(fields - piece_count + 1, fields + 1):
            self.pieces[w] = Piece.from_symbol("M")

    def reset_board(self):
        self._reset_board()

    def _clear_board(self):
        self.pieces = {}

    def clear_board(self):
        """Clears the board."""
        self._clear_board()

    def contains_piece(self, piece_type, color):
        for piece in self.pieces.values():
            if piece.piece_type == piece_type and piece.color == color:
                return True
        return False

    def piece_at(self, square):
        """Gets the :class:`piece <draughts.Piece>` at the given square."""
        return self.pieces.get(square)

    def _set_board_fen(self, fen):
        # Compability with set_fen().
        fen = fen.strip()
        parts = fen.split(":")
        if len(parts) > 3:
            raise ValueError("expected position part of fen, got multiple parts: {}".format(fen))

        # Clear the board.
        self._clear_board()

        # Put pieces on the board.
        for part in parts:
            part_color = BLACK if part[:1].upper() == "B" else WHITE
            part_pieces = part[1:].split(",")
            for part_piece in part_pieces:
                if part_piece[:1].upper() in ["K", "G", "P"]:
                    self.pieces[int(part_piece[1:])] = Piece.from_symbol(part_piece[:1].upper() if part_color == WHITE else part_piece[:1].lower())
                elif len(part_piece) > 0:
                    self.pieces[int(part_piece)] = Piece(MAN, part_color)

    def set_board_fen(self, fen):
        """
        Parses a FEN and sets the board from it.
        :raises: :exc:`ValueError` if the FEN string is invalid.
        """
        self._set_board_fen(fen)