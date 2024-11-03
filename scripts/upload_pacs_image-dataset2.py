import os
import logging
import zipfile
import pydicom
import requests
from kaggle.api.kaggle_api_extended import KaggleApi

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to create the Kaggle API credentials file if it doesn't exist
def setup_kaggle_credentials():
    kaggle_dir = os.path.join(os.path.expanduser("~"), ".kaggle")
    kaggle_json_path = os.path.join(kaggle_dir, "kaggle.json")
    
    if not os.path.exists(kaggle_dir):
        os.makedirs(kaggle_dir)
    
    if not os.path.exists(kaggle_json_path):
        with open(kaggle_json_path, "w") as f:
            f.write('{"username":"example","key":"012345"}')
        os.chmod(kaggle_json_path, 0o600)
        logger.info("Kaggle credentials written to ~/.kaggle/kaggle.json")
    else:
        logger.info("Kaggle credentials already exist.")

# Function to download and unzip the dataset from Kaggle
def download_kaggle_dataset(dataset, download_path):
    try:
        if os.path.exists(download_path) and os.listdir(download_path):
            logger.info(f"Dataset already downloaded in {download_path}")
            return
        
        api = KaggleApi()
        api.authenticate()
        logger.info(f"Downloading {dataset} from Kaggle...")
        zip_path = os.path.join(download_path, f"{dataset}.zip")
        api.competition_download_files(dataset, path=download_path)
        
        # Unzip the downloaded file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_path)
        logger.info(f"Downloaded and extracted {dataset} to {download_path}")
        
        # Remove the zip file after extraction
        os.remove(zip_path)
    except Exception as e:
        logger.error(f"An error occurred while downloading the dataset: {e}")

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
                logger.info(f"Uploaded {dicom_path} to PACS successfully! Response: {response.json()}")
            else:
                logger.error(f"Failed to upload {dicom_path} to PACS. Status Code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        logger.error(f"An error occurred while uploading {dicom_path} to PACS: {e}")

# Main function to download, convert, and upload images
def process_and_upload_images(kaggle_dataset, dataset_directory, orthanc_url, orthanc_user, orthanc_password):
    # Ensure the Kaggle credentials are properly set
    setup_kaggle_credentials()
    
    # Download dataset from Kaggle if not already downloaded
    download_kaggle_dataset(kaggle_dataset, dataset_directory)
    
    # Process and upload only 20 images from each subfolder
    for subset in ['stage_2_test_images', 'stage_2_train_images']:
        subset_path = os.path.join(dataset_directory, subset)
        
        # Check if subset directory exists
        if not os.path.exists(subset_path):
            logger.warning(f"Subset directory {subset_path} not found.")
            continue
        
        dicom_files = [f for f in os.listdir(subset_path) if f.endswith(".dcm")]
        
        for i, dicom_file in enumerate(dicom_files[:20]):  # Only process 20 images
            dicom_path = os.path.join(subset_path, dicom_file)
            logger.info(f"Uploading {dicom_path} to PACS...")
            upload_to_pacs(dicom_path, orthanc_url, orthanc_user, orthanc_password)

# Example usage
kaggle_dataset = "rsna-pneumonia-detection-challenge"  # Kaggle dataset identifier
dataset_directory = "/home/peri/rsna_pneumonia_detection"  # Directory to download and extract dataset
orthanc_url = "http://159.89.235.98:8042"  # URL of your Orthanc PACS server
orthanc_user = "orthanc"  # Orthanc PACS username (update as needed)
orthanc_password = "orthanc"  # Orthanc PACS password (update as needed)

# Process and upload images
process_and_upload_images(kaggle_dataset, dataset_directory, orthanc_url, orthanc_user, orthanc_password)
