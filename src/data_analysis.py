import pandas as pd
import logging

# Constants for DataFrame columns
TERM_COL = "term"
LINK_COL = "link"
ABBRSYN_COL = "abbrSyn"
DEFINITIONS_COL = "definitions"


def fill_group_nulls(group: pd.DataFrame) -> pd.DataFrame:
    """
    Fill null values in a group of rows from the DataFrame.

    Parameters:
    - group: A group of rows from the DataFrame.

    Returns:
    - A DataFrame group with nulls filled using forward and backward filling.
    """
    return group.ffill().bfill()


def analyze_and_fill_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze the DataFrame for null values and fill them by grouping on the 'term' column.

    Parameters:
    - df: The Pandas DataFrame to analyze and fill nulls.

    Returns:
    - A new Pandas DataFrame with null values filled.
    """
    logging.info("Analyzing and filling nulls in the DataFrame.")
    grouped_df = df.groupby(TERM_COL, group_keys=False).apply(fill_group_nulls)
    grouped_df.reset_index(drop=True, inplace=True)
    grouped_df[ABBRSYN_COL] = grouped_df.apply(
        lambda row: row[LINK_COL].split("/")[-1]
        if pd.isna(row[ABBRSYN_COL])
        else row[ABBRSYN_COL],
        axis=1,
    )
    logging.info("Nulls filled in the DataFrame.")
    return grouped_df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame based on specific columns.

    Parameters:
    - df: The Pandas DataFrame from which to remove duplicates.

    Returns:
    - A new Pandas DataFrame with duplicates removed.
    """
    logging.info("Dropping duplicates from the DataFrame.")
    new_df = df.drop_duplicates(
        subset=[TERM_COL, LINK_COL, ABBRSYN_COL, DEFINITIONS_COL], keep="first"
    )
    logging.info("Duplicates dropped from the DataFrame.")
    return new_df


def write_df_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Write the DataFrame to a CSV file.

    Parameters:
    - df: The Pandas DataFrame to write to CSV.
    - output_path: The file path where the CSV will be saved.

    Returns:
    - None
    """
    logging.info(f"Writing DataFrame to {output_path}.")
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"DataFrame has been successfully written to {output_path}")
    except Exception as e:
        logging.error(
            f"An error occurred while writing the DataFrame to {output_path}: {e}"
        )
