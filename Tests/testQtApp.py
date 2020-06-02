import sys
from PySide2.QtWidgets import *
from View.MainWindow.central_widget import CentralWidget
from Model.app_helpers import EasyFrame, ClickAnimationButton


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(300, 200)
        self.setCentralWidget(CentralWidget(self))
        self.myLayout = QHBoxLayout(self)
        self.tab1 = QTabWidget(self)
        self.tab3 = QTabWidget(self)
        self.tab3.setTabPosition(QTabWidget.East)
        self.tab3.tabBarClicked.connect(self.tab_pressed_3)
        self.tab3_minimized = False
        self.tab1.setTabPosition(QTabWidget.East)
        self.tab1.tabBarClicked.connect(self.tab_pressed_1)
        self.tab1_minimized = False
        self.widget1 = EasyFrame()
        self.button1 = ClickAnimationButton()
        self.button1.setText("button 1")
        self.button1.clicked.connect(self.button_test_1)
        self.widget2 = EasyFrame()
        self.button2 = ClickAnimationButton()
        self.button2.setText("button 2")
        self.button2.clicked.connect(self.button_test_2)
        self.widget3 = EasyFrame()
        self.button3 = ClickAnimationButton()
        self.button3.setText("button 3")
        self.button3.clicked.connect(self.button_test_3)
        self.tab1_layout = QVBoxLayout(self.widget1)
        self.tab1_layout.addWidget(self.button1)
        self.tab2_layout = QVBoxLayout(self.widget2)
        self.tab2_layout.addWidget(self.button2)
        self.tab3_layout = QVBoxLayout(self.widget3)
        self.tab3_layout.addWidget(self.button3)
        self.tab1.addTab(self.widget1, "tab 1")
        self.tab1.addTab(self.widget2, "tab 2")
        self.tab3.addTab(self.widget3, "tab 3")
        self.myLayout.addWidget(self.tab1)
        self.myLayout.addWidget(self.tab3)
        # self.myLayout.addWidget(self.button1)
        # self.myLayout.addWidget(self.button2)
        # self.myLayout.addWidget(self.button3)
        self.centralWidget().layout().addLayout(self.myLayout)

    def button_test_1(self):
        print("button 1 pressed")
        msg_box = QDialog()
        # msg_box.setModal(True)
        msg_box.setWindowTitle("Test message box")
        # msg_box.setText("This is a message")
        test_frame = EasyFrame()
        test_layout = QVBoxLayout(test_frame)

        test_button = ClickAnimationButton(test_frame)
        test_button.setText("test button")
        test_button.clicked.connect(self.button_test_2)

        test_layout.addWidget(test_button)

        # msg_box.layout().addWidget(test_layout)
        # msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setLayout(test_layout)

        # msg_box.exec_()
        msg_box.exec()

    def button_test_2(self):
        print("button 2 pressed")

    def button_test_3(self):
        print("button 3 pressed")

    def tab_pressed_1(self):
        print("tab 1 pressed")

    def tab_pressed_2(self):
        print("tab 2 pressed")

    def tab_pressed_3(self):
        print("tab 3 pressed")
        if not self.tab3_minimized:
            self.tab3_minimized = True
            self.tab3.setMaximumWidth(18)
        else:
            self.tab3_minimized = False
            self.tab3.setMaximumWidth(200)

    def tab_pressed_1(self):
        print("tab 3 pressed")
        if not self.tab1_minimized:
            self.tab1_minimized = True
            self.tab1.setMaximumWidth(18)
        else:
            self.tab1_minimized = False
            self.tab1.setMaximumWidth(200)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
