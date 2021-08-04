import maya.OpenMaya as om

from Qt import QtCore

def log_error(text):
    om.MGlobal.displayError("[TWA Tools] {}".format(text))

def log_warning(text):
    om.MGlobal.displayWarning("[TWA Tools] {}".format(text))

def log_output(text):
    om.MGlobal.displayInfo("[TWA Tools] {}".format(text))


class MayaQtLogger(QtCore.QObject):

    VERSION = "0.0.1"

    DEFAULT_SENDER = "TWA Tools"

    output_logged = QtCore.Signal(str)

    def __init__(self, sender=None, log_to_maya=True):
        super(MayaQtLogger, self).__init__()

        self.sender = sender
        self.set_maya_logging_enabled(log_to_maya)

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value if value else MayaQtLogger.DEFAULT_SENDER

    def set_maya_logging_enabled(self, enabled):
        self._log_to_maya = enabled

    def log_error(self, text):
        if self._log_to_maya:
            om.MGlobal.displayError("[{}] {}".format(self.sender, text))

        self.output_logged.emit("[ERROR] {}".format(text))

    def log_warning(self, text):
        if self._log_to_maya:
            om.MGlobal.displayWarning("[{}] {}".format(self.sender, text))

        self.output_logged.emit("[WARNING] {}".format(text))

    def log_output(self, text):
        if self._log_to_maya:
            om.MGlobal.displayInfo("[{}] {}".format(self.sender, text))

        self.output_logged.emit("{}".format(text))


__all__ = ["log_error", "log_warning", "log_output"]
