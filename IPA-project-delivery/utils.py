import pandas as pd


def import_file(file_path):
    return pd.read_csv(file_path)


def export_file(df, file_path):
    df.to_csv(file_path, index=False)
    return file_path