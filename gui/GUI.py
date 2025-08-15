import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QFileDialog,QMainWindow
import pydicom


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #MainWindow.setObjectName("DICOM Viewer")
        MainWindow.resize(1115, 888)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setWindowTitle("DICOM Viewer")
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")

        #metadatatable
        self.metadatatable = QtWidgets.QTableView(self.centralwidget)
        self.metadatatable.setGeometry(QtCore.QRect(680, 0, 431, 841))
        self.metadatatable.setMouseTracking(True)
        self.metadatatable.setTabletTracking(True)
        self.metadatatable.setObjectName("metadatatable")

        #imageviewwer
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 681, 841))
        #self.graphicsView.setObjectName("graphicsView")

        #menubar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1115, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSave = QtWidgets.QMenu(self.menubar)
        self.menuSave.setObjectName("menuSave")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #open new image menu button
        self.actionOpen_new = QtWidgets.QAction(MainWindow)
        self.actionOpen_new.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionOpen_new.setObjectName("actionOpen_new")
        self.actionOpen_new.triggered.connect(self.browse_file)

        #save as JPG menu button
        self.actionSave_as_JPG = QtWidgets.QAction(MainWindow)
        self.actionSave_as_JPG.setObjectName("actionSave_as_JPG")

        #save as DICOM menu button
        self.actionSave_as_DICOM = QtWidgets.QAction(MainWindow)
        self.actionSave_as_DICOM.setObjectName("actionSave_as_DICOM")

        self.menuFile.addAction(self.actionOpen_new)
        self.menuSave.addAction(self.actionSave_as_JPG)
        self.menuSave.addAction(self.actionSave_as_DICOM)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction()) 

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        #MainWindow.setWindowTitle(_translate("DICOM Veiwer", "DICOM Viewer"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSave.setTitle(_translate("MainWindow", "Save"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))

        #open new image menu button
        self.actionOpen_new.setText(_translate("MainWindow", "Open new image"))
        self.actionOpen_new.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))


        self.actionSave_as_JPG.setText(_translate("MainWindow", "Save as JPG"))
        self.actionSave_as_DICOM.setText(_translate("MainWindow", "Save as DICOM"))

    def browse_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open DICOM File", "", "DICOM Files (*.dcm)")
        if file_name:
            # Load the DICOM file
            img = pydicom.dcmread(file_name)
            arryimg = img.pixel_array

            # Convert the pixel array to a QImage
            height, width = arryimg.shape
            bytes_per_line = width * 2  # Assuming 16-bit grayscale
            q_image = QtGui.QImage(arryimg.data, width, height, bytes_per_line, QtGui.QImage.Format_Grayscale16)

            #show the image in the graphics view
            pixmap = QPixmap(q_image)  # Load image
            scene = QGraphicsScene()     # Create a scene
            scene.addPixmap(pixmap)      # Add pixmap to scene
            self.graphicsView.setScene(scene)  # Set the scene on the view
            self.graphicsView.fitInView(scene.sceneRect(), mode=1)
    

def main(self):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

main(Ui_MainWindow)
