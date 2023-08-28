import requests
import logging
import os
import zipfile
from io import BytesIO


def download_zip(url: str) -> bytes:
    """
    Download a ZIP file from a given URL.

    Parameters:
    - url: The URL to download the ZIP file from.

    Returns:
    - A bytes object containing the ZIP file content.
    """
    logging.info(f"Downloading ZIP file from {url}")
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to download ZIP, status code: {response.status_code}")
        raise requests.RequestException("Failed to download ZIP file.")
    logging.info("ZIP file downloaded successfully.")
    return response.content


def extract_zip(zip_content: bytes, output_directory: str) -> list:
    """
    Extract a ZIP file to a specified directory.

    Parameters:
    - zip_content: The ZIP file content as a bytes object.
    - output_directory: The directory where the ZIP file will be extracted to.

    Returns:
    - A list of filenames that were extracted.
    """
    logging.info(f"Extracting ZIP file to {output_directory}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    extracted_files = []
    try:
        with zipfile.ZipFile(BytesIO(zip_content), "r") as zip_ref:
            zip_ref.extractall(output_directory)
            extracted_files = zip_ref.namelist()
    except zipfile.BadZipFile as e:
        logging.error(f"An error occurred while extracting the ZIP file: {e}")
        return []

    logging.info("ZIP file extracted successfully.")
    return extracted_files


def download_and_extract_zip_from_url(url: str, output_directory: str) -> list:
    """
    Download a ZIP file from a given URL and extract it to a specified directory.

    Parameters:
    - url: The URL to download the ZIP file from.
    - output_directory: The directory where the ZIP file will be extracted to.

    Returns:
    - A list of filenames that were extracted.
    """
    try:
        zip_content = download_zip(url)
        extracted_files = extract_zip(zip_content, output_directory)
        return extracted_files
    except (requests.RequestException, zipfile.BadZipFile) as e:
        logging.error(f"An error occurred: {e}")
        return []
