from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsView, QFileDialog, 
                            QMainWindow, QTableWidget, QTableWidgetItem,
                            QSplitter,QLineEdit, QLabel, QVBoxLayout,QPushButton,QHBoxLayout,QComboBox,QMessageBox)

from Controller import get_dicom_image, browse_file, show_image, show_meta_data
from Controller import convert_dicom_to_jpg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1115, 888)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setWindowTitle("DICOM Viewer")
        
        # Create a main horizontal layout
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        
        # Create a splitter for resizable panels
        splitter = QSplitter(QtCore.Qt.Horizontal)
        
        # Image viewer
        self.graphicsView = QtWidgets.QGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        
        # Metadata table
        self.metadatatable = QTableWidget()
        self.metadatatable.setMinimumSize(400, 600)
        self.metadatatable.setObjectName("metadatatable")
        self.metadatatable.setColumnCount(3)
        self.metadatatable.setHorizontalHeaderLabels(['Tag', 'Name', 'Value'])
        self.metadatatable.setColumnWidth(0, 80)
        self.metadatatable.setColumnWidth(1, 150)
        self.metadatatable.setColumnWidth(2, 300)
        
        # Add splitter to layout
       # main_layout.addWidget(splitter)
        self.file_path = None
        # Set central widget
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Initialize current_dicom_path
        self.current_dicom_path = None
        
        # Menu bar setup
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1115, 23))
        self.menubar.setObjectName("menubar")
        
        # Create menus
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSave = QtWidgets.QMenu(self.menubar)
        self.menuSave.setObjectName("menuSave")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        #-----create search bar
        metadata_container = QtWidgets.QWidget()
        metadata_layout = QtWidgets.QVBoxLayout(metadata_container)
        
        # Add search widgets
        self.search_label = QLabel("Search Tags:")
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by tag name or value...")
        self.search_bar.textChanged.connect(self.filter_metadata_table)
        
        # Add search widgets to layout
        metadata_layout.addWidget(self.search_label)
        metadata_layout.addWidget(self.search_bar)
        metadata_layout.addWidget(self.metadatatable)
        
        # Create splitter and add widgets
        splitter = QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.graphicsView)
        splitter.addWidget(metadata_container)
        splitter.setSizes([700, 400])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Create actions
        self.actionOpen_new = QtWidgets.QAction(MainWindow)
        self.actionOpen_new.setObjectName("actionOpen_new")
        self.actionOpen_new.triggered.connect(self.handle_open_new)
        
        
        
        self.actionSave_as_JPG = QtWidgets.QAction(MainWindow)
        self.actionSave_as_JPG.setObjectName("actionSave_as_JPG")
        
        self.actionSave_as_DICOM = QtWidgets.QAction(MainWindow)
        self.actionSave_as_DICOM.setObjectName("actionSave_as_DICOM")
        self.actionSave_as_JPG.triggered.connect(self.save_as_jpg)
        self.menuSave.addAction(self.actionSave_as_JPG)
        
        # Add actions to menus
        self.menuFile.addAction(self.actionOpen_new)
        self.menuSave.addAction(self.actionSave_as_JPG)
        self.menuSave.addAction(self.actionSave_as_DICOM)
        
        # Add menus to menubar
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        
        # Set menubar and statusbar
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DICOM Viewer"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSave.setTitle(_translate("MainWindow", "Save"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionOpen_new.setText(_translate("MainWindow", "Open new image"))
        self.actionOpen_new.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.actionSave_as_JPG.setText(_translate("MainWindow", "Save as JPG"))
        self.actionSave_as_DICOM.setText(_translate("MainWindow", "Save as DICOM"))
    
    def handle_open_new(self):
        file_path = browse_file()  # Call browse_file() once
        self.current_dicom_path = file_path  # Update current_dicom_path
        show_image(self, file_path)  # Pass the file path to show_image
        show_meta_data(self, file_path)  # Pass the file path to show_meta_data



    def filter_metadata_table(self, text):
        """Filter the metadata table based on search text"""
        text = text.lower()
        
        for row in range(self.metadatatable.rowCount()):
            tag_item = self.metadatatable.item(row, 0)
            name_item = self.metadatatable.item(row, 1)
            value_item = self.metadatatable.item(row, 2)
            
            if not all((tag_item, name_item, value_item)):
                continue
                
            # Check if search text matches any of the columns
            tag_matches = text in tag_item.text().lower()
            name_matches = text in name_item.text().lower()
            value_matches = text in value_item.text().lower()
            
            # Show/hide row based on matches
            self.metadatatable.setRowHidden(row, not (tag_matches or name_matches or value_matches))
    
    def save_as_jpg(self):
        """Handle JPG conversion"""
        if not hasattr(self, 'current_dicom_path'):
            QMessageBox.warning(None, "Error", "No DICOM file loaded!")
            return
            
        jpg_path, _ = QFileDialog.getSaveFileName(
            None, "Save JPG", "", "JPEG Files (*.jpg)")
            
        if jpg_path:
            if not jpg_path.endswith('.jpg'):
                jpg_path += '.jpg'
                
            if convert_dicom_to_jpg(self.current_dicom_path, jpg_path):
                QMessageBox.information(None, "Success", "Saved as JPG!")
            else:
                QMessageBox.critical(None, "Error", "Conversion failed!")

