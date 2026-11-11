
from pandas import DataFrame
from sklearn.model_selection import train_test_split

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def prepare_data(df: DataFrame, **kwargs):
    """
    Split Iris data into training and testing datasets.
    """
    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test


@test
def test_output(X_train, X_test, y_train, y_test) -> None:
    assert len(X_train) == 120
    assert len(X_test) == 30
    assert len(y_train) == 120
    assert len(y_test) == 30
    assert y_train.nunique() == 3
    assert y_test.nunique() == 3

