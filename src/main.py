import logging
from data_downloader import download_and_extract_zip_from_url
from data_preprocessing import load_json_data, preprocess_data
from data_analysis import analyze_and_fill_nulls, drop_duplicates, write_df_to_csv
import config

# Initialize logging
logging.basicConfig(level=logging.INFO)


def main() -> None:
    logging.info("Starting the data pipeline.")

    # Download and extract ZIP file
    if not download_and_extract_zip_from_url(config.URL, config.TEMP_DIRECTORY):
        logging.error("Failed to download or extract ZIP file. Exiting.")
        return

    # Load and preprocess JSON data
    try:
        json_data = load_json_data(config.JSON_FILE_PATH)
    except FileNotFoundError:
        logging.error(f"JSON file not found at {config.JSON_FILE_PATH}. Exiting.")
        return

    processed_data = preprocess_data(json_data)

    # Analyze and further process data
    analyzed_data = analyze_and_fill_nulls(processed_data)
    final_data = drop_duplicates(analyzed_data)

    # Write the final DataFrame to a CSV file
    output_file_path = f"{config.OUTPUT_DIRECTORY}/nist_glossary.csv"
    write_df_to_csv(final_data, output_file_path)

    logging.info("Data pipeline completed successfully.")


if __name__ == "__main__":
    main()
