###########################################################
# Code from https://github.com/caleblf/catan-setup
###########################################################

#!/usr/bin/env python3

import random
import json

#from asciicanvas import ASCIICanvas

###########################################################
# Drawable objects (HexTiles)
###########################################################


class _ASCIICanvasRow(bytearray):
    """Row for the ASCIICanvas.
    This class's __setitem__ does not set any whitespace values.
    """

    def _set_byte(self, i, c):
        """Set the byte at index i to c only if c is not whitespace."""
        if isinstance(c, int):
            if bytes((c,)).isspace():
                return
        elif c.isspace():
            return
        bytearray.__setitem__(self, i, c)

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            for i, c in zip(range(*index.indices(len(self))), val):
                self._set_byte(i, c)
        else:
            self._set_byte(index, val)


class ASCIICanvas:

    def __init__(self, rows, cols):
        """Return a rows*cols ASCIICanvas."""
        self.rows = rows
        self.cols = cols
        self.grid = [_ASCIICanvasRow(b' '*cols)
                     for i in range(rows)]

    def __getitem__(self, indices):
        """Get items from the canvas.
        Subscripting takes two comma-separated args, either or both
        of which may be a slice or int.
        Syntax:
                AC[0, 1]
                AC[0:1, 2]
                AC[0, 1:2]
                AC[0:1, 2:3]
                etc.
        """
        try:
            r, c = indices
            if isinstance(r, slice):
                return [self.grid[i][c] for i in range(*r.indices(self.rows))]
            else:
                return self.grid[r][c]
        except (ValueError, TypeError):
            raise TypeError(
                'ASCIICanvas indices must be 2-tuple of int and/or slice, not %s' % type(indices))

    def __setitem__(self, indices, val):
        """Set values in the canvas. Whitespace characters are ignored.
        Uses the same subscripting syntax as ASCIICanvas.__getitem__
        """
        pass
        try:
            r, c = indices
            if isinstance(r, slice):
                for row, val_row in zip(self.grid[r], val):
                    row[c] = val_row
            else:
                self.grid[r][c] = val
        except (ValueError, TypeError):
            raise TypeError(
                'ASCIICanvas indices must be 2-tuple of int and/or slice, not %s' % type(indices))

    def __repr__(self):
        return 'ASCIIGrid(%d, %d)' % (self.rows, self.cols)

    def __str__(self):
        return '\n'.join(row.decode('ascii') for row in self.grid)
###########################################################
# Drawable objects (HexTiles)
###########################################################


class NotDrawableError(Exception):
    pass


class HexTile(object):
    """An object drawable on an ASCIICanvas"""

    height = 0
    width = 0

    numbered = False

    def draw(self, row, col, canvas):
        raise NotDrawableError


class EmptySpace(HexTile):
    """An empty space which is not drawn on the ASCIICanvas"""

    height = 0
    width = 0

    def __repr__(self):
        return "EmptySpace()"

    def draw(self, row, col, canvas):
        pass


EMPTY = EmptySpace()


class TerrainTile(HexTile):
    """Represents a single Catan terrain tile."""

    height = 7
    width = 13

    numbered = True

    roll_pips = {
        2:  1,
        3:  2,
        4:  3,
        5:  4,
        6:  5,
        8:  5,
        9:  4,
        10: 3,
        11: 2,
        12: 1
    }

    def __init__(self, terrain="Desert", roll=0):
        self.terrain = terrain
        self.roll = roll

    def pips(self):
        """Return the number of pips on this tile, based on its roll value."""
        return self.roll_pips.get(self.roll, 0)

    def __repr__(self):
        return "TerrainTile({:s}, {:s})".format(repr(self.terrain), repr(self.roll))

    def draw(self, row, col, canvas):
        r"""
        Draw self onto the ASCIICanvas, with upper-left corner (row, col).
        A 13 (columns) by 7 (rows) space is required to draw a TerrainTile.
        TerrainTiles are drawn in the following format, where the % marks the
        upper-left corner and is not drawn:

                %  _______
                  /       \
                 /         \
                / -terrain- \
                \ --roll--- /
                 \ -pips-- /
                  \_______/

        """
        canvas[row:row+self.height, col:col+self.width] = [
            rb'   _______   ',
            rb'  /       \  ',
            rb' /         \ ',
            r'/ {:^9s} \\'.format(self.terrain).encode('ascii'),
            r'\ {:^9d} /'.format(self.roll).encode('ascii'),
            r' \ {:^7s} / '.format('*'*self.pips()).encode('ascii'),
            rb'  \_______/  ',
        ]


class Harbor(HexTile):
    """Represents a Catan harbor tile"""

    height = 7
    width = 13

    def __init__(self, direction="N", resource="?", ratio=None):
        self.direction = direction
        self.setResource(resource)
        if ratio:
            self.ratio = ratio

    def setResource(self, resource):
        self.resource = resource
        if resource == "?":
            self.ratio = (3, 1)
        else:
            self.ratio = (2, 1)

    def __repr__(self):
        return "Harbor({0:s}, {1:s}, {2})".format(repr(self.direction),
                                                  repr(self.resource),
                                                  self.ratio)

    def draw(self, row, col, canvas):
        r"""
        Draw self onto the canvas, with upper-left corner (row, col).
        A 13 (columns) by 7 (rows) space is required to draw a Harbor.
        Harbors are drawn in the following format, where the % marks the
        upper-left corner and is not drawn. This example has a direction
        of NE:

                %       __
                        \ \
                         \ \
                     -:-  \ \
                   ------- \/



        """
        canvas[row+3:row+5, col+3:col+11] = [
            r'{0:>3d}:{1:<3d}'.format(*self.ratio).encode('ascii'),
            r'{:^7s}'.format(self.resource).encode('ascii'),
        ]
        if self.direction == "N":
            canvas[row:row+2, col+2:col+11] = [
                rb' _______ ',
                rb'/_______\\',
            ]
        elif self.direction == "NE":
            canvas[row:row+5, col+8:col+13] = [
                rb'__   ',
                rb'\ \  ',
                rb' \ \ ',
                rb'  \ \\',
                rb'   \/',
            ]
        elif self.direction == "SE":
            canvas[row+3:row+7, col+8:col+13] = [
                rb'   /\\',
                rb'  / /',
                rb' / / ',
                rb'/_/  ',
            ]
        elif self.direction == "S":
            canvas[row+5:row+7, col+2:col+11] = [
                rb'_________',
                rb'\_______/',
            ]
        elif self.direction == "SW":
            canvas[row+3:row+7, col:col+5] = [
                rb'/\   ',
                rb'\ \  ',
                rb' \ \ ',
                rb'  \_\\',
            ]
        elif self.direction == "NW":
            canvas[row:row+5, col:col+5] = [
                rb'   __',
                rb'  / /',
                rb' / / ',
                rb'/ /  ',
                rb'\/   ',
            ]
        else:
            raise ValueError('Invalid harbor direction: %s' % self.direction)


###########################################################
# File input
###########################################################

def to_roll(c):
    """
    Converts a roll identifier to a roll number.
    2 -> 2
    3 -> 3
    4 -> 4
    5 -> 5
    6 -> 6
    7 -> 7
    8 -> 8
    9 -> 9
    0 -> 10
    1 -> 11
    t -> 12
    """
    if c == "0":
        return 10
    elif c == "1":
        return 11
    elif c.isdigit():
        return int(c)
    elif c == "t":
        return 12
    else:
        raise ValueError


def read_board(filename):
    """
    Reads a catan board from a file.
    If the file does not exist, raises FileNotFoundError.
    If the file is not properly formatted, raises ValueError.
    """
    file = open(filename)

    random_terrain_tiles = []
    random_harbors = []

    def make_tile(row, col, c):
        """
        Make a tile based on the given character at the given position in
        the checkerboard grid.
        """
        if (row + col) % 2 != 0:
            # Ignore characters on alternating spaces in a checkerboard pattern
            return EMPTY

        def make_random_terrain_tile():
            t = TerrainTile()
            random_terrain_tiles.append(t)
            return t

        def make_random_harbor(direction):
            h = Harbor(direction)
            random_harbors.append(h)
            return h

        def BadFormat():
            raise ValueError

        return {
            ' ': lambda: EMPTY,
            '\n': lambda: EMPTY,
            'T': lambda: make_random_terrain_tile(),
            'N': lambda: make_random_harbor('N'),
            'S': lambda: make_random_harbor('S'),
            'e': lambda: make_random_harbor('SE'),
            'E': lambda: make_random_harbor('NE'),
            'w': lambda: make_random_harbor('SW'),
            'W': lambda: make_random_harbor('NW'),
            'H': lambda: TerrainTile(terrain='Hills'),
            'P': lambda: TerrainTile(terrain='Pasture'),
            'F': lambda: TerrainTile(terrain='Forest'),
            'f': lambda: TerrainTile(terrain='Fields'),
            'M': lambda: TerrainTile(terrain='Mountains'),
            'D': lambda: TerrainTile(terrain='Desert'),
            'O': lambda: TerrainTile(terrain='Sea'),
            'G': lambda: TerrainTile(terrain='GoldField')
        }.get(c, lambda: BadFormat())()

    hexes = [[make_tile(row, col, c) for col, c in enumerate(line)]
             for row, line in enumerate(file)]

    # number tiles
    for row, line in enumerate(file):
        for col, c in enumerate(line)[1::2]:
            if not c.isspace() and hexes[row][col - 1].numbered:
                hexes[row][col - 1].roll = to_roll(c)

    return (hexes, random_terrain_tiles, random_harbors)


def read_random_qtys(filename):
    """
    Reads a set of random generation parameters from a file.
    If the file does not exist, raises FileNotFoundError.
    If the file is improperly formatted, raises ValueError.
    """
    file = open(filename)
    data = json.load(file)
    try:
        terrain_quantities = data['terrain']
        harbor_res_quantities = data['harbors']
        roll_quantities = {int(roll): qty
                           for roll, qty in data['rolls'].items()}
        return (terrain_quantities, harbor_res_quantities, roll_quantities)
    except KeyError:
        raise ValueError


def load_scenario(name):
    try:
        return (*read_board('scenarios/{}.catanboard'.format(name)),
                *read_random_qtys('scenarios/{}.catanqtys'.format(name)))
    except FileNotFoundError:
        quit('File Not Found')
    except ValueError:
        quit('Invalid File Format')


###########################################################
# Game board operations
###########################################################


class GameBoard(object):
    """Represents a Catan game board."""

    pip_threshold = 5  # tiles with more pips than this cannot be neighbors

    def __init__(self, hexes, random_terrain_tiles=[], random_harbors=[],
                 terrain_quantities={}, harbor_res_quantities={},
                 roll_quantities={}):
        self.board = hexes

        self.random_terrain_tiles = random_terrain_tiles
        self.random_harbors = random_harbors

        self.terrain_quantities = terrain_quantities
        self.harbor_res_quantities = harbor_res_quantities
        self.roll_quantities = roll_quantities

        # Randomize terrain
        terrains = [terrain
                    for terrain, qty in terrain_quantities.items()
                    for i in range(qty)]
        if len(terrains) < len(random_terrain_tiles):
            raise ValueError  # bad file format; too few terrains

        random.shuffle(terrains)
        for tile in random_terrain_tiles:
            tile.terrain = terrains.pop(0)

        # Randomize harbors
        harbor_resources = [res
                            for res, qty in harbor_res_quantities.items()
                            for i in range(qty)]
        if len(harbor_resources) < len(random_harbors):
            raise ValueError  # bad file format; too few harbors

        random.shuffle(harbor_resources)
        for harbor in random_harbors:
            harbor.setResource(harbor_resources.pop(0))

    def number_tiles(self, verbose=True):
        """
        Number the tiles in self.board, using the roll_quantities with quantities
        in self.roll_quantities.
        """
        if verbose:
            print("Numbering Tiles", end="")
        rolls = [roll
                 for roll, qty in self.roll_quantities.items()
                 for i in range(qty)]
        while True:
            if verbose:
                print(".", end="")
            rolls_scrambled = rolls[:]
            random.shuffle(rolls_scrambled)

            for row in self.board:
                for tile in row:
                    if tile.numbered and tile.terrain not in ('Desert', 'Sea'):
                        try:
                            tile.roll = rolls_scrambled.pop(0)
                        except IndexError:
                            raise ValueError  # bad file format; too few rolls

            if self.valid():
                if verbose:
                    print("Done.")
                return

    def valid(self):
        """
        Returns whether the board numbering is valid, i.e. whether
        no tiles above the pip threshold are neighbors.
        """
        for row, tiles in enumerate(self.board):
            for col, tile in enumerate(tiles):
                if tile.numbered and tile.pips() >= self.pip_threshold:
                    for n in self.neighbors(col, row):
                        if n.numbered and n.pips() >= self.pip_threshold:
                            return False
        return True

    def tile_at(self, col, row):
        if row < 0 or row >= len(self.board):
            return None
        if col < 0 or col >= len(self.board[row]):
            return None
        return self.board[row][col]

    def neighbors(self, col, row):
        """Returns a generator of neighbors of the tile at the given location."""
        for (c, r) in [(col, row - 2),
                       (col, row + 2),
                       (col - 1, row - 1),
                       (col - 1, row + 1),
                       (col + 1, row - 1),
                       (col + 1, row + 1)]:
            t = self.tile_at(c, r)
            if t != None:
                yield t

    def print(self):
        """Prints the board to standard output."""

        canvas_height = max([tile.height + (row * 3)
                             for row, tiles in enumerate(self.board)
                             for tile in tiles])
        canvas_width = max([tile.width + (col*10)
                            for tiles in self.board
                            for col, tile in enumerate(tiles)])

        canvas = ASCIICanvas(canvas_height, canvas_width)

        for row, cells in enumerate(self.board):
            for col, cell in enumerate(cells):
                cell.draw(row*3, col*10, canvas)

        print(canvas)

###########################################################
# Script body
###########################################################


if __name__ == '__main__':
    board = GameBoard(*load_scenario('default'))
    board.number_tiles()
    board.print()
    print()
