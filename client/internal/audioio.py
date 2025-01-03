import sys

import pyaudio
import audioop

from .audiobuffer import AudioBuffer

RATE = 40000
CHANNELS = 1 if sys.platform == 'darwin' else 2
LATENCY = 0.02
BUFFER_SIZE = int(RATE * CHANNELS * 2 * LATENCY * 3)

class AudioIO:
    def __init__(self):
        self.volume = 1
        self.latency = LATENCY
        self.outputBuffer = AudioBuffer(BUFFER_SIZE)
        self.inputBuffers: dict[bytes, AudioBuffer] = {}
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(2),
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            stream_callback=self._get_callback(),
            start=False
        )

    def start(self):
        self.stream.start_stream()

    def read(self) -> bytes:
        return bytes(self.outputBuffer.get_max())
    
    def write(self, data: bytes):
        id_len: int = data[0]
        id: bytes = data[1:1+id_len]
        self.inputBuffers[id] = self.inputBuffers.get(id, AudioBuffer(BUFFER_SIZE))
        self.inputBuffers[id].put(data[1+id_len:])

    def _get_mixed(self, size: int):
        if len(self.inputBuffers) == 0:
            return bytes([0 for _ in range(size)])
        keys = list(self.inputBuffers.keys())
        out = bytes(self.inputBuffers.get(keys[0]).get(size))
        for key in keys[1:]:
            out = audioop.add(out, bytes(self.inputBuffers.get(key).get(size)), 2)
        return audioop.mul(out, 2, self.volume)
    
    def _get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.outputBuffer.put(in_data)
            data = self._get_mixed(frame_count*CHANNELS*2)
            return (data, pyaudio.paContinue)
        
        return callback