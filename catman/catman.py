from struct import unpack, calcsize
from collections import OrderedDict

class BinaryReader:
    def __init__(self, filename):
        self.filename = filename
        self.fid      = None

    def open(self):
        self.fid = open(self.filename, 'br')

    def close(self):
        self.fid.close()

    def short(self, num=1):
        return unpack('h'*num, self.fid.read(2*num))[0]

    def integer(self, num=1):
        return unpack('i'*num, self.fid.read(4*num))[0]

    def double(self, num=1):
        return unpack('d'*num, self.fid.read(8*num))[0]

    def single(self, num=1):
        return unpack('f'*num, self.fid.read(4*num))[0]

    def string(self, num=1, encoding='latin1'):
        if num:
            return b''.join(unpack('c'*num, self.fid.read(num))).decode(encoding)
        else:
            return ''

    def sigchar(self, num=1):
        return unpack('b'*num, self.fid.read(1*num))[0]


class CatmanReader(BinaryReader):
    def __init__(self, filename, onlyHeader=False, head=-1):
        self.filename = filename
        self.onlyHeader = onlyHeader
        self.head = head
        self.Update(self.onlyHeader, self.head)

    def Update(self, onlyHeader=0, head=0):
        ''' Reread the entire CATMAN file '''
        self.open()
        fileInfo = self._read_header()
        channels = [self._read_chHeader() for i in range(fileInfo['nChannels'])]

        chBitSize = [ch['length']*calcsize('d') for ch in channels]
        chDataOffset = [fileInfo['data_offset'] + sum(chBitSize[:i])
                        for i in range(fileInfo['nChannels'])]
        fileInfo['chDataOffset'] = chDataOffset

        if not onlyHeader:
            for n, ch in enumerate(channels):
                self.fid.seek(chDataOffset[n])
                if head > 0:
                    assert (head < ch['length']), \
                        "Head data must be lower than channel length!"
                chRange = range(ch['length']) if head < 0 \
                          else range(head)
                ch['data'] = [self.double() for i in chRange]
        self.close()

        fileInfo['channels'] = channels
        self.__dict__.update(fileInfo)

    def _read_header(self):
        ''' Read general header of the file '''

        header = OrderedDict()

        header['version'] = self.short()
        assert (header['version'] > 5010), "Only Catman 5.0+ is supported"

        header['data_offset'] = self.integer()
        header['comment']     = self.string(self.short())
        header['reserved']    = [self.string(self.short()) for i in range(32)]
        header['nChannels']   = self.short()
        header['maxChannelLength'] = self.integer()
        header['chOffset'] = [self.integer() for i in range(header['nChannels'])]
        header['redFactor'] = self.integer()

        return header

    def _read_chHeader(self):
        ''' Read the header of one channel '''
        chInfo = OrderedDict()
        chInfo['ID']        = self.short()
        chInfo['length']    = self.integer()
        chInfo['name']      = self.string(self.short())
        chInfo['units']     = self.string(self.short())
        chInfo['comment']   = self.string(self.short())
        chInfo['format']    = self.short()
        chInfo['width']     = self.short()
        chInfo['date']      = self.double()
        chInfo['header']    = self.string(self.integer())
        chInfo['lin_mode']  = self.sigchar()
        chInfo['lin_scale'] = self.sigchar()
        chInfo['lin_nPts']  = self.sigchar()
        chInfo['lin_pts']   = [self.double() for i in range(chInfo['lin_nPts'])]
        chInfo['thermoType']= self.short()
        chInfo['formula']   = self.string(self.short())
        chInfo['SoDBinfo']  = self.string(self.integer())

        return chInfo


class SpreadCatmanReader(CatmanReader):
    def __init__(self, filename, nPoints):
        self.filename = filename
        self.nPoints = nPoints
        self.Update()

    def Update(self):
        super().Update(onlyHeader=True)

        self.open()
        for n, ch in enumerate(self.channels):
            simpleDataPoints = self._getChannelPoints(nChannel=n)
            ch['data'] = [self._getDataPoint(pos)
                          for pos in simpleDataPoints]
        self.close()

    def _getChannelPoints(self, nChannel):
        ''' Calc the distributed points in the channel '''
        ch = self.channels[nChannel]
        chLength = ch['length']*calcsize('d')
        chDataOffset = self.chDataOffset[nChannel]

        datPositions = list(range(chDataOffset, chDataOffset+chLength, 8))
        chRate = len(datPositions) // self.nPoints

        return [datPositions[i] for i in range(0, len(datPositions), chRate)]


    def _getDataPoint(self, pos):
        ''' Moves to the position and read the data point '''
        self.fid.seek(pos)
        return self.double()
