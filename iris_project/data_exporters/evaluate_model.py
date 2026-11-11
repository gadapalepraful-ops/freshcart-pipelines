
import pandas as pd
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_exporter
def evaluate_model(df, **kwargs):
    actual = df['actual']
    predicted = df['predicted']

    matrix = confusion_matrix(actual, predicted)

    print("\nConfusion Matrix:")
    print(matrix)

    metrics = pd.DataFrame({
        'Metric': [
            'Accuracy',
            'Precision (Weighted)',
            'Recall (Weighted)',
            'F1 Score (Weighted)'
        ],
        'Score': [
            accuracy_score(actual, predicted),
            precision_score(actual, predicted, average='weighted', zero_division=0),
            recall_score(actual, predicted, average='weighted', zero_division=0),
            f1_score(actual, predicted, average='weighted', zero_division=0)
        ]
    })

    print("\nEvaluation Metrics:")
    print(metrics.to_string(index=False))

    metrics.to_csv('iris_metrics.csv', index=False)

    print("\nSaved metrics to iris_metrics.csv")

    return metrics


@test
def test_output(metrics) -> None:
    assert metrics is not None
    assert len(metrics) == 4
    assert metrics['Score'].between(0, 1).all()
