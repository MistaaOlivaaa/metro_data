from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIRECTORY = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIRECTORY = PROJECT_ROOT / "data" / "processed"


def load_table(filename: str, processed: bool = False) -> pd.DataFrame:
    """Load one GTFS table from the raw or processed data directory."""
    directory = PROCESSED_DIRECTORY if processed else RAW_DIRECTORY
    return pd.read_csv(directory / filename, dtype=str)


def load_all_raw() -> dict[str, pd.DataFrame]:
    """Load every raw GTFS TXT file available in data/raw."""
    return {
        file.name: pd.read_csv(file, dtype=str)
        for file in sorted(RAW_DIRECTORY.glob("*.txt"))
    }
