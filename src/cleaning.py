from pathlib import Path

import pandas as pd


def clean_table(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Normalize headers and text fields, remove empty and duplicate rows."""
    cleaned = dataframe.copy()
    cleaned.columns = cleaned.columns.str.strip()

    for column in cleaned.select_dtypes(include="str"):
        cleaned[column] = cleaned[column].str.strip()

    return cleaned.replace(r"^\s*$", pd.NA, regex=True).dropna(how="all").drop_duplicates()


def clean_directory(input_directory: Path, output_directory: Path) -> None:
    """Clean every TXT table in a directory and save it as CSV."""
    output_directory.mkdir(parents=True, exist_ok=True)
    for input_file in sorted(input_directory.glob("*.txt")):
        clean_table(pd.read_csv(input_file, dtype=str)).to_csv(
            output_directory / f"{input_file.stem}_clean.csv", index=False
        )
