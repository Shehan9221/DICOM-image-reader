import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow


def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    #Controller(ui)  # Attach controller

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()