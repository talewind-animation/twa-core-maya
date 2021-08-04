import logging

from pyseq import Sequence

log = logging.getLogger('pyudim')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

default_format = '%h%f%t'
tile_sign = '#'
missing_tile_sign = '-'

class UdimError(Exception):
    """
    Special exception for Udim errors
    """
    pass

class Udim(Sequence):
    """
    Extends pyseq.Sequence class with methods that handle udim tiles.
    """
    def __init__(self, *args):
        super(Udim, self).__init__(*args)
        self._check_range()
        self._channel = self._find_channel()

    @property
    def channel(self):
        return self._channel

    def __str__(self):
        return self.format(default_format)

    def reIndex(self, *args, **kwargs):
        '''
        Disabled reindexing of sequence.
            Raises:
                (Exception): UdimError
        '''
        log.debug("reIndexing is disabled")
        raise UdimError("Can't reindex udim items")

    def tiles(self):
        '''
        Returns list of tiles.
            Returns:
                (list): existing tiles

        '''
        return self.frames()

    def _find_channel(self):
        return self.format('%h%t')

    def _check_range(self):
        '''
        Checks the range of the sequence. Udim tiles can only be from 1001-9999.
            Raises:
                (Exception): UdimError
        '''
        if not self.start() > 1000 or not self.end() < 10000:
            raise UdimError('UDIM range must be from 1001 to 9999')
        log.debug("UDIM range ok!")

    def show_tiles(self):
        '''
        Returns string with tiles diagram like in a uv editor.

        4  - # # # # - - - - -
        3  # # # - - # - - - #
        2  # # # # - # # - - -
        1  # # # - - - - - - -
           1 2 3 4 5 6 7 8 9 10

        '''
        rows = []

        end = self.end()
        rounding = 10-int(str(end)[-1:])
        end = end+rounding+1

        row = []
        for tile in range(self.start(), end):
            if tile in self.tiles():
                row.append(tile_sign)
            else:
                row.append(missing_tile_sign)

            if (tile-1)%10 == 9:
                rows.append(row)
                row = []

        result = ''
        for n, row in enumerate(reversed(rows)):
            result += '{}  '.format(len(rows)-n)
            result += ' '.join(row)
            result += '\n'
        result += '   '
        result += ' '.join([str(i) for i in range(1, 11)])
        return result
