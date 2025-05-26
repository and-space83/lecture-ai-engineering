import os
import pickle
import numpy as np
from sklearn.metrics import accuracy_score

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
NEW_MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model.pkl")
REFERENCE_MODEL_PATH = os.path.join(MODEL_DIR, "titanic_model_reference.pkl")


def test_model_regression():
    """モデルの精度が過去モデルより劣化していないかチェック"""
    if not (os.path.exists(NEW_MODEL_PATH) and os.path.exists(REFERENCE_MODEL_PATH)):
        import pytest

        pytest.skip("モデルファイルが不足しています")

    with open(NEW_MODEL_PATH, "rb") as f:
        new_model = pickle.load(f)
    with open(REFERENCE_MODEL_PATH, "rb") as f:
        ref_model = pickle.load(f)

    # 同じデータで比較
    import pandas as pd
    from sklearn.model_selection import train_test_split

    data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/Titanic.csv"))
    X = data.drop("Survived", axis=1)
    y = data["Survived"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    acc_new = accuracy_score(y_test, new_model.predict(X_test))
    acc_ref = accuracy_score(y_test, ref_model.predict(X_test))

    print(f"New Model Accuracy: {acc_new}")
    print(f"Reference Model Accuracy: {acc_ref}")

    # 許容差（1%以下）を超えて劣化していないこと
    assert acc_new >= acc_ref - 0.01, "新しいモデルが劣化しています"
