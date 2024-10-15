import os
import pydicom
import numpy as np
from PIL import Image, UnidentifiedImageError
import requests
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi

# Function to create the Kaggle API credentials file if it doesn't exist
def setup_kaggle_credentials():
    kaggle_dir = os.path.join(os.path.expanduser("~"), ".kaggle")
    kaggle_json_path = os.path.join(kaggle_dir, "kaggle.json")
    
    # Create the .kaggle directory if it doesn't exist
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)
    
    # Write the credentials to kaggle.json if it doesn't exist
    if not os.path.exists(kaggle_json_path):
        with open(kaggle_json_path, "w") as f:
            f.write('{"username":"example","key":"012345"}')
        os.chmod(kaggle_json_path, 0o600)  # Set permissions
        print("Kaggle credentials written to ~/.kaggle/kaggle.json")
    else:
        print("Kaggle credentials already exist.")

# Function to download dataset from Kaggle
def download_kaggle_dataset(dataset, download_path):
    try:
        # Check if dataset is already downloaded
        if os.path.exists(download_path) and os.listdir(download_path):
            print(f"Dataset already downloaded in {download_path}")
            return
        
        api = KaggleApi()
        api.authenticate()
        print(f"Downloading {dataset} from Kaggle...")
        api.dataset_download_files(dataset, path=download_path, unzip=True)
        print(f"Downloaded and extracted {dataset} to {download_path}")
    except Exception as e:
        print(f"An error occurred while downloading the dataset: {e}")

# Function to convert a JPEG image to DICOM
def convert_jpeg_to_dicom(jpeg_path, dicom_path):
    try:
        img = Image.open(jpeg_path)
        img_array = np.array(img)

        # Create a DICOM dataset
        file_meta = pydicom.Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'  # Secondary Capture Image Storage
        file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

        ds = FileDataset(dicom_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

        # Set DICOM attributes
        ds.PatientName = "ChestXRay^Patient"
        ds.PatientID = "123456"
        ds.Modality = "CR"  # Computed Radiography
        ds.StudyInstanceUID = pydicom.uid.generate_uid()
        ds.SeriesInstanceUID = pydicom.uid.generate_uid()
        ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
        ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
        ds.ContentDate = datetime.now().strftime('%Y%m%d')
        ds.ContentTime = datetime.now().strftime('%H%M%S')

        # Image-specific attributes
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.Rows, ds.Columns = img_array.shape[:2]
        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0

        # Convert to grayscale if it's a color image
        if len(img_array.shape) == 3:
            img_array = np.mean(img_array, axis=2).astype(np.uint8)

        ds.PixelData = img_array.tobytes()

        # Save the DICOM file
        ds.save_as(dicom_path, write_like_original=False)
        print(f"Converted {jpeg_path} to {dicom_path}")
    except UnidentifiedImageError:
        print(f"Skipping invalid image file: {jpeg_path}")
    except Exception as e:
        print(f"An error occurred while converting {jpeg_path} to DICOM: {e}")



# Function to upload DICOM to Orthanc PACS with basic authentication
def upload_to_pacs(dicom_path, orthanc_url, orthanc_user, orthanc_password):
    try:
        with open(dicom_path, 'rb') as dicom_file:
            headers = {'Content-Type': 'application/dicom'}
            response = requests.post(
                f"{orthanc_url}/instances",
                data=dicom_file.read(),
                headers=headers,
                auth=(orthanc_user, orthanc_password)
            )
            if response.status_code == 200:
                print(f"Uploaded {dicom_path} to PACS successfully! Response: {response.json()}")
            else:
                print(f"Failed to upload {dicom_path} to PACS. Status Code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while uploading {dicom_path} to PACS: {e}")

# Main function to download, convert, and upload images
def process_and_upload_images(kaggle_dataset, dataset_directory, output_directory, orthanc_url, orthanc_user, orthanc_password):
    # Ensure the Kaggle credentials are properly set
    setup_kaggle_credentials()
    
    # Download dataset from Kaggle if not already downloaded
    download_kaggle_dataset(kaggle_dataset, dataset_directory)
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Process all JPEG images in the dataset
    for root, dirs, files in os.walk(dataset_directory):
        for file in files:
            if file.endswith(".jpeg") or file.endswith(".jpg"):
                jpeg_path = os.path.join(root, file)

                # Skip non-image files from __MACOSX directories or hidden files
                if "._" in file or "__MACOSX" in root:
                    print(f"Skipping non-image file: {jpeg_path}")
                    continue

                dicom_filename = file.replace(".jpeg", ".dcm").replace(".jpg", ".dcm")
                dicom_path = os.path.join(output_directory, dicom_filename)

                # Check if the DICOM file already exists
                if os.path.exists(dicom_path):
                    print(f"Skipping conversion: DICOM file {dicom_path} already exists for {jpeg_path}")
                else:
                    print(f"Converting {jpeg_path} to {dicom_path}...")
                    # Convert JPEG to DICOM
                    convert_jpeg_to_dicom(jpeg_path, dicom_path)
                
                # Upload DICOM to PACS (ensure it only uploads if conversion was successful)
                if os.path.exists(dicom_path):
                    print(f"Uploading {dicom_path} to PACS...")
                    upload_to_pacs(dicom_path, orthanc_url, orthanc_user, orthanc_password)
                else:
                    print(f"Skipping upload: DICOM file {dicom_path} does not exist")

# Example usage
kaggle_dataset = "paultimothymooney/chest-xray-pneumonia"  # Kaggle dataset identifier
dataset_directory = "/home/peri/chest_xray"  # Directory to download and extract dataset
output_directory = "/home/peri/chest_xray/output_dicom"  # Directory to store the DICOM files
orthanc_url = "http://localhost:8042"  # URL of your Orthanc PACS server
orthanc_user = "orthanc"  # Orthanc PACS username (update as needed)
orthanc_password = "orthanc"  # Orthanc PACS password (update as needed)

# Process and upload images
process_and_upload_images(kaggle_dataset, dataset_directory, output_directory, orthanc_url, orthanc_user, orthanc_password)
