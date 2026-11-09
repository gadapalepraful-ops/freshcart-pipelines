import pandas as pd
from sklearn.model_selection import train_test_split

def transform(df):
    train, test = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["target"]
    )

    df = df.copy()
    df["split"] = ""

    df.loc[train.index, "split"] = "train"
    df.loc[test.index, "split"] = "test"

    return df