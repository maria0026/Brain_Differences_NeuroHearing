import yaml
import pandas as pd

def load_config(path="config.yaml"):
    # Read in the configuration file
    with open(path) as p:
        config = yaml.safe_load(p)
    return config


def convert_to_datetime(df, column, suffix):
    col = f"{column}_{suffix}"
    df[col] = pd.to_datetime(df[col], errors="coerce")
    return df