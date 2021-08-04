from Qt import QtWidgets

import maya.cmds as cmds
from twa_maya.gui.workspace_control import WorkspaceControl

class SampleMayaDialog(QtWidgets.QWidget):

    WINDOW_TITLE = "Maya Dialog"
    UI_NAME = "SampleMayaDialog"

    dlg_instance = None

    @classmethod
    def display(cls):
        if cls.dlg_instance:
            cls.dlg_instance.show_workspace_control()
        else:
            cls.dlg_instance = SampleMayaDialog()

    @classmethod
    def get_workspace_control_name(cls):
        return "{}WorkspaceControl".format(cls.UI_NAME)

    def __init__(self):
        super(SampleMayaDialog, self).__init__()

        self.setObjectName(self.__class__.UI_NAME)
        self.__geometry = None

        self.configure_window()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.create_workspace_control()

    def configure_window(self):
        self.setMinimumSize(200, 100)

    def create_widgets(self):
        self.btn=QtWidgets.QPushButton("Push ME!!")

    def create_layout(self):
        self.lyt = QtWidgets.QVBoxLayout(self)
        self.lyt.addWidget(self.btn)

    def create_connections(self):
        pass

    def create_workspace_control(self):
        self.workspace_control_instance = WorkspaceControl(self.get_workspace_control_name())
        if self.workspace_control_instance.exists():
            self.workspace_control_instance.restore(self)
        else:
            self.workspace_control_instance.create(self.WINDOW_TITLE, self, ui_script="from gui.maya_dialog import SampleMayaDialog\nSampleMayaDialog.display()")

    def show_workspace_control(self):
        self.workspace_control_instance.set_visible(True)


    def showEvent(self, e):
        super(SampleMayaDialog, self).showEvent(e)
        if self.__geometry:
            self.restoreGeometry(self.__geometry)

    def closeEvent(self, e):
        if isinstance(self, SampleMayaDialog):
            super(SampleMayaDialog, self).closeEvent(e)

            self.__geometry = self.saveGeometry()


if __name__ == "__main__":

    workspace_control_name = SampleMayaDialog.get_workspace_control_name()
    if cmds.window(workspace_control_name, exists=True):
        cmds.deleteUI(workspace_control_name)

    dialog = SampleMayaDialog()

