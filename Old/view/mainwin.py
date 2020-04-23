from PySide2.QtWidgets import (QMainWindow, QWidget, QPushButton,
                               QVBoxLayout, QGroupBox, QGridLayout,
                               QLabel, QLineEdit, QMdiArea, QTextEdit, QSpacerItem,
                               QSizePolicy, QAction, QStatusBar, QSlider)
from PySide2.QtGui import QCloseEvent
from PySide2.QtCore import Qt
from asyncio import Event
from Old.devices.template.view import mdi_win


class MainWindow(QMainWindow):
    def __init__(self, close_event_callback: Event):
        super(MainWindow, self).__init__()
        self.close_event_callback = close_event_callback
        self.resize(700, 900)
        # main_wgt
        main_wgt = QWidget()
        self.setCentralWidget(main_wgt)
        self.setWindowTitle("RS Companion")
        # main_window/main_wgt <- main_grid

        grid = QGridLayout()
        main_wgt.setLayout(grid)

        # mdi
        self.mdi_win = mdi_win.MDIWidget()
        mdi = QMdiArea()

        # slider
        slider = QSlider()
        slider.setOrientation(Qt.Horizontal)

        # main_window/main_wgt-main_grid <- gb_control_bar
        grid.addWidget(self.set_controls(), 0, 0)
        grid.addWidget(self.set_key_flag(), 0, 1)
        grid.addWidget(self.set_notes(), 0, 2)
        grid.addWidget(self.set_information(), 0, 4)
        grid.addItem(QSpacerItem(300, 0, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding), 0, 3)
        grid.addWidget(mdi, 1, 0, 1, 5)
        grid.addWidget(slider, 2, 0, 1, 5)
        grid.setRowStretch(1, 1)

        # menu
        self.set_menu()

        # QMDI subwindow
        # sub = QMdiSubWindow()
        # sub.resize(655, 515)
        # self.mid_text = QLabel("Nothing yet...")
        # self.mid_text.setText("what??")
        # sub.setWidget(self.mid_text)
        # sub.setWindowTitle("VOG COM32")
        # sub.setWindowIcon(self.create_icon_by_color(QColor("transparent")))

        mdi.addSubWindow(self.mdi_win)

    def creat_status_bar(self):
        self.sb = QStatusBar()
        self.setStatusBar(self.sb)
        self.sb.showMessage("Hello", 2000)

    def update_status_bar(self, msg):
        self.sb.showMessage(msg, 2000)

    def set_menu(self):

        menubar = self.menuBar()

        # FILE
        file = menubar.addMenu('&File')

        new_exp = QAction(
            "&New", self, triggered=lambda: self.update_status_bar("New"))
        new_exp.setShortcut("Ctrl+n")
        file.addAction(new_exp)

        open_exp = QAction("&Open", self, triggered=self.clicked)
        open_exp.setShortcut("Ctrl+o")
        file.addAction(open_exp)

        save_exp = QAction("&Save", self, triggered=self.clicked)
        save_exp.setShortcut("Ctrl+s")
        file.addAction(save_exp)

        file.addSeparator()

        configure = QAction("&Configure", self, triggered=self.clicked)
        file.addAction(configure)

        # HELP
        help = menubar.addMenu('&Help')
        check_update = QAction("&Check for Updates",
                               self, triggered=self.clicked)
        help.addAction(check_update)

    def clicked(self):
        print("clicked")

    def set_notes(self):
        group = QGroupBox("Notes")
        vert = QVBoxLayout()
        group.setLayout(vert)
        group.setFixedSize(250, 130)

        entry = QTextEdit()
        entry.setMaximumHeight(50)
        vert.addWidget(entry)

        btn = QPushButton("Post")
        btn.setToolTip("Messages are posted to the output file...")
        vert.addWidget(btn)

        return group

    def set_mdi(self):
        mdi = QMdiArea()

        return mdi

    def set_key_flag(self):
        group = QGroupBox("Key Flag")
        vert = QVBoxLayout()
        group.setLayout(vert)
        group.setFixedSize(130, 130)

        label = QLabel("NA")
        vert.addWidget(label)

        return group

    def set_information(self):
        group = QGroupBox("Information")
        grid = QGridLayout()
        group.setLayout(grid)
        group.setFixedSize(200, 130)

        start_t = QLabel("Experiment Start Time: ")
        grid.addWidget(start_t, 0, 0)

        start_v = QLabel("NA")
        grid.addWidget(start_v, 0, 2)

        block_n = QLabel("Block Number: ")
        grid.addWidget(block_n, 1, 0)

        block_v = QLabel("NA")
        grid.addWidget(block_v, 1, 2)

        spacer = QSpacerItem(100, 200, QSizePolicy.Minimum,
                             QSizePolicy.Expanding)
        grid.addItem(spacer, 2, 1)

        return group

    def set_controls(self):
        group = QGroupBox("Experiment")
        grid = QGridLayout()
        group.setLayout(grid)
        group.setFixedSize(200, 130)

        btn = QPushButton("Run")
        grid.addWidget(btn, 0, 0)
        btn.setMinimumHeight(50)
        btn.setMinimumWidth(120)

        btn = QLineEdit("DEFAULT")
        grid.addWidget(btn, 1, 0)

        return group

    def closeEvent(self, event:QCloseEvent):
        self.close_event_callback.set()


