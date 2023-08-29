import logging
from data_downloader import download_and_extract_zip_from_url
from data_preprocessing import load_json_data, preprocess_data
from data_analysis import analyze_and_fill_nulls, drop_duplicates, write_df_to_csv
import config
from create_kaggle_metadata import create_kaggle_metadata

# Initialize logging
logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Main function to run the data pipeline."""
    logging.info("Starting the data pipeline.")

    # Step 1: Download and extract ZIP file
    if not download_and_extract_zip_from_url(config.URL, config.TEMP_DIRECTORY):
        logging.error("Failed to download or extract ZIP file. Exiting.")
        return

    # Step 2: Load and preprocess JSON data
    try:
        json_data = load_json_data(config.JSON_FILE_PATH)
    except FileNotFoundError:
        logging.error(f"JSON file not found at {config.JSON_FILE_PATH}. Exiting.")
        return
    processed_data = preprocess_data(json_data)

    # Step 3: Analyze and further process data
    analyzed_data = analyze_and_fill_nulls(processed_data)
    final_data = drop_duplicates(analyzed_data)

    # Step 4: Write the final DataFrame to a CSV file
    output_file_path = f"{config.OUTPUT_DIRECTORY}/nist_glossary.csv"
    write_df_to_csv(final_data, output_file_path)

    logging.info("Data pipeline completed successfully.")

    # Step 5: Create Kaggle metadata file
    create_kaggle_metadata(
        title=config.DATASET_TITLE,
        subtitle=config.DATASET_SUBTITLE,
        username=config.KAGGLE_USERNAME,
        dataset_name=config.KAGGLE_DATASET_NAME,
        output_directory=config.OUTPUT_DIRECTORY,
    )


if __name__ == "__main__":
    main()
