from typing import Any, Dict

import json
import os
import logging


def create_kaggle_metadata(
    title: str, subtitle: str, username: str, dataset_name: str, output_directory: str
) -> None:
    """
    Create Kaggle dataset metadata file.

    Parameters:
    - title: The title of the Kaggle dataset.
    - subtitle: The subtitle or description of the Kaggle dataset.
    - username: The username of the Kaggle user who will own the dataset.
    - dataset_name: The name of the dataset.
    - output_directory: The directory where the metadata JSON will be saved.

    Returns:
    - None
    """
    metadata: Dict[str, Any] = {
        "title": title,
        "subtitle": subtitle,
        "description": "This dataset contains a comprehensive list of glossary terms provided by the National Institute of Standards and Technology (NIST). It serves as a rich resource for researchers, security experts, and policy makers to understand and standardize terminologies in various domains including cybersecurity, information security, and more.\n\n## Data Source\nThe data is sourced from NIST's official website: [NIST Glossary](https://csrc.nist.gov/csrc/media/glossary/glossary-export.zip).\n\n## Data Columns\n- `term`: The glossary term.\n- `link`: The link to the term's detail page.\n- `abbrSyn`: Abbreviations or synonyms for the term.\n- `definitions`: Definitions of the term.\n\n## Usage\nThis dataset can be used for educational purposes, research, and to standardize terminologies in scientific papers, articles, or projects.",  # noqa: E501
        "id": f"{username}/{dataset_name}",  # Replace <username> and <dataset-name> as appropriate
        "licenses": [{"name": "apache-2.0"}],
        "keywords": [
            "beginner",
        ],
        "annotations": {
            "maintainer": "Ron Mallory",
            "source": "https://csrc.nist.gov/csrc/media/glossary/glossary-export.zip",
        },
        "resources": [
            {
                "path": "nist_glossary.csv",
                "description": "The NIST Glossary of Key Information Security Terms",
            }
        ],
    }

    metadata_path: str = os.path.join(output_directory, "dataset-metadata.json")

    try:
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)
        logging.info(f"Kaggle metadata file has been written to {metadata_path}")
    except Exception as e:
        logging.error(f"An error occurred while writing the Kaggle metadata file: {e}")
