from AnyQt.QtWidgets import QAction, QMenu
from AnyQt.QtCore import Qt

from Orange.canvas import config

from orangecanvas.application.canvasmain import CanvasMainWindow
from orangecanvas.registry import get_style_sheet, get_global_registry
from orangecanvas.application.outputview import TextStream

from orangecontrib.blue_whale.i18n_config import *


def __(key):
    return i18n.t("bluewhale.canvasmain." + key)


__SESSION = {"SESSION": ""}


def login(way=None):
    global __SESSION
    if __SESSION.get('SESSION'):  # 登录状态，用户点击则是退出，
        set_session({'SESSION': None}, messge=__("sign_in"))
    else:
        if not way:
            get_session()


login_action = QAction(
    __("sign_in"),
    objectName="action-login",
    toolTip=__("login"),
    triggered=login,
)


def get_user_session():
    global __SESSION
    from orangecontrib.blue_whale.widgets.utils.login import MainWindow
    window = MainWindow(__SESSION)
    window.exec_()
    return __SESSION.get('SESSION')


def set_session(value, messge=__("sign_in")):
    global __SESSION, login_action
    __SESSION.update(value)
    login_action.setText(messge)


def get_session(key='SESSION'):
    global __SESSION, login_action
    if __SESSION.get(key):
        return __SESSION[key]

    if not get_user_session():
        return None
    login_action.setText(__("sign_out"))
    return __SESSION.get(key)


def get_session_value(key='SESSION'):
    global __SESSION
    return __SESSION.get(key)


def set_service():
    from orangecontrib.blue_whale.widgets.utils.service_window import ServiceWindow
    window = ServiceWindow()
    window.exec_()


class BWCanvasMainWindow(CanvasMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global login_action

        menubar = self.menuBar()
        server_menu = QMenu(
            self.tr(__("service")), menubar, objectName="server-menu"
        )
        self.settings_action = QAction(
            __("service_settings"), self,
            objectName="action-settings",
            toolTip=__("service_settings_tip"),
            triggered=set_service
        )

        server_menu.addAction(login_action)
        server_menu.addAction(self.settings_action)
        menubar.addMenu(server_menu)
        self.setMenuBar(menubar)

    def open_case(self, filename):
        """
        Open and load a '*.report' from 'filename'
        """
        widget_registry = get_global_registry()
        if self.is_transient():
            window = self
        else:
            window = self.create_new_window()
        window.setWindowModified(True)
        window.setWindowModified(False)

        window.setStyleSheet(get_style_sheet())
        window.setAttribute(Qt.WA_DeleteOnClose)
        window.setWindowIcon(config.application_icon())
        window.connect_output_stream(TextStream())
        window.set_widget_registry(widget_registry)

        window.open_example_scheme(filename)

    def closeEvent(self, event):
        super().closeEvent(event)
