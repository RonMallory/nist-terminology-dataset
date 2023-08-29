import json
import re
import pandas as pd
from pandas import json_normalize
from typing import List, Dict, Union


# Function to remove HTML tags
def remove_html_tags(text: str) -> str:
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def load_json_data(file_path: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    """
    Load the JSON data from a given file path.

    Parameters:
    - file_path: The path to the JSON file.

    Returns:
    - A dictionary containing the JSON data.
    """
    with open(file_path, "r", encoding="utf-8-sig") as f:
        json_data = json.load(f)
    return json_data


def preprocess_data(
    json_data: Dict[str, Union[str, List[Dict[str, str]]]]
) -> pd.DataFrame:
    """
    Preprocess the JSON data to create a flattened DataFrame.

    Parameters:
    - json_data: The JSON data as a dictionary.

    Returns:
    - A Pandas DataFrame containing the preprocessed data.
    """
    # Flatten the 'parentTerms' column to focus on the parent terms
    flattened_parent_terms_df = json_normalize(
        json_data, record_path="parentTerms", sep="_"
    )

    # Drop 'note' and 'seeAlso' columns
    flattened_parent_terms_df = flattened_parent_terms_df.drop(
        columns=["note", "seeAlso"]
    )

    # Initialize a list to store the new rows for the fully flattened data
    new_rows = []

    # Loop through each row in the DataFrame containing parent terms
    for idx, row in flattened_parent_terms_df.iterrows():
        term = row["term"]
        link = row["link"]

        # Flatten 'abbrSyn'
        abbr_list = row["abbrSyn"]
        if abbr_list is not None and isinstance(abbr_list, list):
            for abbr in abbr_list:
                new_row = {
                    "term": term,
                    "link": link,
                    "abbrSyn": abbr.get("text", None),
                    "definitions": None,
                }
                new_rows.append(new_row)

        # Flatten 'definitions'
        def_list = row["definitions"]
        if def_list is not None and isinstance(def_list, list):
            for definition in def_list:
                new_row = {
                    "term": term,
                    "link": link,
                    "abbrSyn": None,
                    "definitions": definition.get("text", None),
                }
                new_rows.append(new_row)

        # Case when both 'abbrSyn' and 'definitions' are None or not lists
        if (abbr_list is None or not isinstance(abbr_list, list)) and (
            def_list is None or not isinstance(def_list, list)
        ):
            new_row = {
                "term": term,
                "link": link,
                "abbrSyn": None,
                "definitions": None,
            }
            new_rows.append(new_row)

    # Create a new DataFrame from the list of new rows
    fully_flattened_df = pd.DataFrame(new_rows)

    # Change all values to lowercase
    fully_flattened_df = fully_flattened_df.applymap(
        lambda x: x.lower().strip() if isinstance(x, str) else x
    )

    # Group the DataFrame by the 'term' column and use 'ffill' and 'bfill' to fill NaN values within each group
    fully_flattened_df = fully_flattened_df.groupby("term", group_keys=False).apply(
        lambda group: group.ffill().bfill()
    )

    # Reset the index for the DataFrame
    fully_flattened_df.reset_index(drop=True, inplace=True)

    # Extract the last part of the URL in the 'link' column and use it to fill NaN values in 'abbrSyn'
    fully_flattened_df["abbrSyn"] = fully_flattened_df.apply(
        lambda row: row["link"].split("/")[-1]
        if pd.isna(row["abbrSyn"])
        else row["abbrSyn"],
        axis=1,
    )

    # Update the 'definitions' column based on the condition for 'abbrSyn'
    fully_flattened_df["definitions"] = fully_flattened_df.apply(
        lambda row: f"{row['abbrSyn']}: {row['link'].split('/')[-1].replace('_', ' ')}"
        if (pd.isna(row["definitions"]))
        else row["definitions"],
        axis=1,
    )

    # Identify and drop duplicated rows based on all given columns
    fully_flattened_df.drop_duplicates(
        subset=["term", "link", "abbrSyn", "definitions"], keep="first", inplace=True
    )

    # remove html tags from 'term' column
    fully_flattened_df["term"] = fully_flattened_df["term"].apply(remove_html_tags)

    return fully_flattened_df
