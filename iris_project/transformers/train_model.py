
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def train_model(data, **kwargs):
    X_train, X_test, y_train, y_test = data

    max_depth = int(kwargs.get('max_depth', 3))

    model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"max_depth: {max_depth}")
    print(f"test_accuracy: {accuracy:.4f}")

    results = pd.DataFrame({
        'actual': y_test.to_numpy(),
        'predicted': predictions,
        'accuracy': accuracy
    })

    return results

@test
def test_output(df) -> None:
    assert df is not None
    assert len(df) == 30
    assert 'actual' in df.columns
    assert 'predicted' in df.columns
    assert df['accuracy'].between(0, 1).all()
    assert df['accuracy'].iloc[0] >= 0.90
