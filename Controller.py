from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QFileDialog, QMainWindow
from Dicom import get_dicom_image
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QPixmap
import pydicom
from PIL import Image
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_voi_lut
import numpy as np

def browse_file():
    file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open DICOM File", "", "DICOM Files (*.dcm)")
    if file_name:
        return file_name
    
def show_image(self, file_name):
        img = get_dicom_image(file_name)  # Must be uint16 and normalized

        height, width = img.shape
        q_image = QtGui.QImage(img.tobytes(), width, height, width * 2, QtGui.QImage.Format_Grayscale16)

        pixmap = QtGui.QPixmap.fromImage(q_image)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)

        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

def show_meta_data(self,file_name):
    dicom_file = pydicom.dcmread(file_name)
    self.metadatatable.setRowCount(0)
    self.metadatatable.setColumnCount(3)
    self.metadatatable.setHorizontalHeaderLabels(['Tag', 'Name' , 'Value'])
    self.metadatatable.setColumnWidth(0, 80)  # Tag column
    self.metadatatable.setColumnWidth(1, 150)  # Name column
    self.metadatatable.setColumnWidth(2, 300)  # Value column



    for elem in dicom_file:
        if elem.name != "PixelData":
            tag_str = str(elem.tag)
            name_str = str(elem.name)
            value_str = str(elem.value)

            # Truncate long values for better performance
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            if not value_str.strip():
                continue
            row_position = self.metadatatable.rowCount()
            self.metadatatable.insertRow(row_position)
            self.metadatatable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(tag_str))
            self.metadatatable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(name_str))
            self.metadatatable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(value_str))

def search_table(self, text):
    text = text.lower()
    for row in range(self.metadatatable.rowCount()):
        match_found = False
        for column in range(self.metadatatable.columnCount()):
            item = self.metadatatable.item(row, column)
            if item and text in item.text().lower():
                match_found = True
        self.metadatatable.setRowHidden(row, not match_found)

def convert_dicom_to_jpg(dicom_path, jpg_path):
    """
    Convert DICOM file to JPG image with medical image processing
    Args:
        dicom_path: Path to source DICOM file
        jpg_path: Destination path for JPG file
    Returns:
        bool: True if success, False if failed
    """
    try:
        # Read DICOM file
        ds = pydicom.dcmread(dicom_path)
        
        if 'PixelData' not in ds:
            raise ValueError("DICOM file lacks pixel data")
            
        # Apply VOI LUT if available (windowing)
        img = apply_voi_lut(ds.pixel_array, ds)
        
        # Normalize to 8-bit range
        img = ((img - img.min()) / (img.max() - img.min())) * 255.0
        img = img.astype(np.uint8)
        
        # Handle both grayscale and color images
        mode = 'RGB' if len(img.shape) == 3 else 'L'
        Image.fromarray(img, mode).save(jpg_path)
        return True
        
    except Exception as e:
        print(f"Conversion error: {str(e)}")
        return False