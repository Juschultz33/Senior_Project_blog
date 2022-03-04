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
