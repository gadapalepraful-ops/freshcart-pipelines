
import pandas as pd
from pathlib import Path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


OUTPUT_FILE = 'iris_predictions.csv'


@data_exporter
def save_results(df, **kwargs):
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved predictions to {OUTPUT_FILE}")
    return df


@test
def test_output(df) -> None:
    assert df is not None
    assert len(df) == 30
    assert Path(OUTPUT_FILE).exists()
