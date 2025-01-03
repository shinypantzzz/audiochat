class AudioBuffer:
    """ byte FIFO buffer """
    def __init__(self, max_length):
        self._buf = bytearray()
        self._max_length = max_length

    def put(self, data):
        overlap = len(data) + len(self) - self._max_length
        if overlap <= 0:
            self._buf.extend(data)
        else:
            self._buf[:overlap] = b''
            self._buf.extend(data[-self._max_length:])

    def get(self, size):
        data = self._buf[:size] + bytearray([0 for _ in range(size - len(self))])
        self._buf[:size] = b''
        return data

    def get_max(self):
        data = self._buf[:]
        self._buf[:] = b''
        return data

    def __len__(self):
        return len(self._buf)