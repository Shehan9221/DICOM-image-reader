import pydicom
import numpy as np

def get_dicom_image(file_path):
    """
    Load a DICOM file and return pixel data as a uint16 array suitable for QImage.
    """
    dicom_file = pydicom.dcmread(file_path)
    pixel_data = dicom_file.pixel_array.astype(np.float32)

    # Normalize to 0–65535 for 16-bit display
    pixel_data -= pixel_data.min()
    if pixel_data.max() != 0:
        pixel_data /= pixel_data.max()
    pixel_data *= 65535

    return pixel_data.astype(np.uint16)

def get_dicom_metadata(file_path):
    """
    Load a DICOM file and return its metadata.
    
    Parameters:
    file_path (str): Path to the DICOM file.
    
    Returns:
    dict: Metadata from the DICOM file.
    """
    # Read the DICOM file
    dicom_file = pydicom.dcmread(file_path)
    
    # Extract metadata
    metadata = {tag: dicom_file.get(tag) for tag in dicom_file.keys()}
    
    return metadata