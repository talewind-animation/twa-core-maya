import uuid
import pymel.core as pm


class MayaMenu(object):

    """
    Easily create or edit maya menues and commands.

    example usage:
        my_menu = MayaMenu.add_menu('MyMenu')
        my_menu.add_command('hello', 'print("Hello World")')
        my_menu.separator()
        my_menu.add_command('modeling/primitives/box', 'cmds.polyCube()')
        my_menu.separator('modeling/primitives')
        my_menu.add_command('modeling/primitives/sphere', 'cmds.polySphere()')
    """

    @staticmethod
    def maya_window():
        """
        Get maya main window widget

        Returns
        -------
        Maya main window widget
        """

        return pm.language.melGlobals['gMainWindow']

    @classmethod
    def add_menu(cls, name):
        """
        Check if menu already exists delete it and create an instance of MayaMenu(this) object.

        Parameters
        ----------
        name (str) : menu name

        Returns
        -------
        MayaMenu
        """

        maya_window = cls.maya_window()
        if pm.menu(name, exists=True, parent=maya_window):
            pm.deleteUI(pm.menu(name, e=True, deleteAllItems=True))

        return cls(pm.menu(name, parent=maya_window, tearOff=True))

    def __init__(self, menu):
        self._menu = None
        self.menu = menu

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, menu):
        if isinstance(menu, pm.uitypes.Menu):
            self._menu = menu
        elif isinstance(menu, str):
            if pm.menu(menu, exists=True, parent=self.maya_window()):
                self._menu = pm.menu(menu, e=True)

    def __str__(self):
        return self.menu.name() if self.menu else None

    def __repr__(self):
        return str(self)

    def add_command(self, name, command, label=None, icon=None):
        if '/' in name:
            subdirs, name = name.rsplit('/', 1)
            parent = self.__populate_subdirs(subdirs, self.menu)
        else:
            parent = self.menu

        if not label:
            label = name.title()
        if not icon:
            icon = ""
        pm.menuItem(name, command=command, label=label, image=icon, parent=parent)

    def separator(self, place=None):
        parent = self.__populate_subdirs(place, self.menu)
        pm.menuItem('{}_div'.format(uuid.uuid4().hex[:8]), divider=True, parent=parent)

    def __populate_subdirs(self, subdirs, parent):
        if not subdirs:
            return parent
        prep = subdirs.split('/', 1)
        if len(prep) > 1:
            current, subdirs = prep
        else:
            current = prep
            subdirs = None
        if not pm.menu(current, exists = True):
            parent = pm.menuItem(current, subMenu=True, tearOff=True, parent=parent)
        else:
            parent = pm.menu(current, e = True)
        return self.__populate_subdirs(subdirs, parent)
