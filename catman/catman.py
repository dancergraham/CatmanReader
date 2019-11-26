from struct import unpack

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
    def __init__(self, filename):
        self.filename = filename
        self.Update()

    def Update(self):
        ''' Reread the entire CATMAN file '''
        self.open()
        fileInfo = self._read_header()
        channels = [self._read_chHeader() for i in range(fileInfo['nChannels'])]
        self.fid.seek(fileInfo['data_offset'])
        for ch in channels:
            ch['data'] = [self.double() for i in range(ch['length'])]
        self.close()

        fileInfo['channels'] = channels
        self.__dict__.update(fileInfo)

    def _read_header(self):
        ''' Read general header of the file '''

        header = {}

        header['version'] = self.short()
        assert (header['version'] > 5010), "Only Catman 5.0+ is supported"

        header['data_offset'] = self.integer()
        header['comment']     = self.string(self.short())
        header['reserved']    = [self.string(self.short()) for i in range(32)]
        header['nChannels']   = self.short()
        header['maxChannelLength'] = self.integer()
        header['chOffet'] = [self.integer() for i in range(header['nChannels'])]
        header['redFactor'] = self.integer()

        return header

    def _read_chHeader(self):
        ''' Read the header of one channel '''
        chInfo = {}
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
