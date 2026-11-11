
from sklearn.datasets import load_iris
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_iris_data(**kwargs) -> DataFrame:
    """
    Load the Iris dataset from scikit-learn.
    """
    iris = load_iris(as_frame=True)
    df = iris.frame

    return df


@test
def test_output(df) -> None:
    assert df is not None
    assert len(df) == 150, 'Iris dataset should contain 150 rows'
    assert 'target' in df.columns, 'Target column is missing'
    assert df['target'].nunique() == 3, 'Expected 3 target classes'
