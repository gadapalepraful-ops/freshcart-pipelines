
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def validate_iris(df: DataFrame, **kwargs) -> DataFrame:
    assert df is not None
    assert df.isnull().sum().sum() == 0
    assert df['target'].nunique() == 3

    print("Iris dataset validation successful.")
    print(f"Rows: {len(df)}")
    print(f"Features: {len(df.columns) - 1}")
    print(f"Target classes: {df['target'].nunique()}")

    return df


@test
def test_output(df) -> None:
    assert len(df) == 150
    assert df.isnull().sum().sum() == 0
    assert df['target'].nunique() == 3
