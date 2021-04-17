
from fnmatch import fnmatchcase

from rtmidi import MidiIn

from plover.machine.base import ThreadedStenotypeBase
from plover import log

BASE_NOTES = 'C C# D D# E F F# G G# A A# B'.split()
NUM_OCTAVES = 10


class MidiStenotype(ThreadedStenotypeBase):

    PORT = '*'

    KEYS_LAYOUT = '''
        C-2 C#-2 D-2 D#-2 E-2 F-2 F#-2 G-2 G#-2 A-2 A#-2 B-2
        C-1 C#-1 D-1 D#-1 E-1 F-1 F#-1 G-1 G#-1 A-1 A#-1 B-1
        C0  C#0  D0  D#0  E0  F0  F#0  G0  G#0  A0  A#0  B0
        C1  C#1  D1  D#1  E1  F1  F#1  G1  G#1  A1  A#1  B1
        C2  C#2  D2  D#2  E2  F2  F#2  G2  G#2  A2  A#2  B2
        C3  C#3  D3  D#3  E3  F3  F#3  G3  G#3  A3  A#3  B3
        C4  C#4  D4  D#4  E4  F4  F#4  G4  G#4  A4  A#4  B4
        C5  C#5  D5  D#5  E5  F5  F#5  G5  G#5  A5  A#5  B5
        C6  C#6  D6  D#6  E6  F6  F#6  G6  G#6  A6  A#6  B6
        C7  C#7  D7  D#7  E7  F7  F#7  G7  G#7  A7  A#7  B7
        C8  C#8  D8  D#8  E8  F8  F#8  G8
    '''

    def __init__(self, params):
        super().__init__()
        self._params = params
        self._midi = MidiIn()
        self._midi.set_callback(self._on_message, None)
        self._note_to_key = []
        for octave in range(10):
            for note in 'C C# D D# E F F# G G# A A# B'.split():
                self._note_to_key.append(note + str(octave - 2))
        self._pressed = set()
        self._stroke = set()

    def run(self):
        log.info('available ports: %s', ', '.join(self._midi.get_ports()))
        port_glob = self._params['port'].lower()
        for port, port_name in enumerate(self._midi.get_ports()):
            if fnmatchcase(port_name.lower(), port_glob):
                break
        else:
            log.warning('no port found, matching: %s', port_glob)
            self._error()
            return
        log.info('opening port: %s', port_name)
        try:
            self._midi.open_port(port)
        except:
            log.warning('error opening port: %s', port_name, exc_info=True)
            self._error()
            return
        self._ready()
        self.finished.wait()
        self._midi.close_port()

    def _on_message(self, params, data):
        message, delta = params
        log.debug('message: %r', message)
        if message[0] not in (0x80, 0x90):
            return
        # Note: some keyboards indicate key release by sending a note on
        # message with a velocity of zero (instead of a note off message).
        pressed = message[0] == 0x90 and message[2] != 0
        key = self._note_to_key[message[1]]
        log.debug('%s %s', key, 'pressed' if pressed else 'released')
        if pressed:
            self._pressed.add(key)
            self._stroke.add(key)
            return
        self._pressed.discard(key)
        if self._pressed:
            return
        stroke = self._stroke
        self._stroke = set()
        steno_keys = self.keymap.keys_to_actions(stroke)
        if not steno_keys:
            return
        log.debug('stroke: %r', steno_keys)
        self._notify(steno_keys)

    @classmethod
    def get_option_info(cls):
        """Get the default options for this machine."""
        return {
            'port': (cls.PORT, str),
        }


def test_machine(port=None):
    import sys
    import time
    if port is None:
        port = sys.argv[1] if len(sys.argv) > 1 else '*'
    log.set_level(log.DEBUG)
    machine = MidiStenotype({'port': port})
    machine.start_capture()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        machine.stop_capture()


if __name__ == '__main__':
    test_machine()
