from copy import copy

from PyQt5.QtCore import QVariant, pyqtSignal
from PyQt5.QtWidgets import QWidget

from rtmidi import MidiIn

from plover_midi.gui_qt.midi_widget_ui import Ui_MidiWidget


class MidiOption(QWidget, Ui_MidiWidget):

    valueChanged = pyqtSignal(QVariant)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._value = {}
        self.port.addItems(MidiIn().get_ports())

    def setValue(self, value):
        self._value = copy(value)
        port = value['port']
        if port is not None:
            self.port.setCurrentText(port)

    def _update(self, field, value):
        self._value[field] = value
        self.valueChanged.emit(self._value)

    def on_port_changed(self, value):
        self._update('port', value)
