import joblib
import pandas as pd
from dotenv import load_dotenv
import os
# Os and dotenv works hand in hand, as .env is has environment variables, to access em, we need os library

from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib

load_dotenv()
# this function was used used once to drop columns, ignore this as the csv has already been created. The columns were dropped for simplicity
def makenewcsv():
    data = pd.read_csv(os.getenv("DATA_PATH"))
    dcols = [
        "Access_to_Resources",
        "Parental_Involvement",
        "Motivation_Level",
        "Internet_Access",
        "Tutoring_Sessions",
        "Family_Income",
        "Teacher_Quality",
        "School_Type",
        "Peer_Influence",
        "Physical_Activity",
        "Learning_Disabilities",
        "Parental_Education_Level",
        "Distance_from_Home",
        "Gender",
    ]

    new_data = data.drop(columns=dcols)

    new_data.to_csv("/home/san/studentperformancepredictor/datasets/newData.csv", index=False)


def train_and_save_models():
    data = pd.read_csv(os.getenv("DATA_PATH"))

    X = data.drop("Exam_Score", axis=1)
    y = data["Exam_Score"]

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=None
    )

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_features),
            ("categorical", OneHotEncoder(), categorical_features),
        ]
    )

    # Define models in a dictionary
    models = {
        "Linear": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=1.0, max_iter=10000),
    }

    model_paths = {
        "Linear": os.getenv("LINEAR_MODEL_PATH"),
        "Ridge": os.getenv("RIDGE_MODEL_PATH"),
        "Lasso": os.getenv("LASSO_MODEL_PATH"),
    }

    for name, model in models.items():
        pipeline = Pipeline([("preprocessor", preprocessor), ("regressor", model)])

        # Cross-validation
        scores = cross_val_score(
            pipeline, X_train, y_train, scoring="neg_mean_squared_error", cv=8
        )
        print(f"{name}: {-scores.mean():.2f}")

        # Fit on full training data
        pipeline.fit(X_train, y_train)

        # Savin
        save_path = model_paths[name]
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(pipeline, save_path)
        print(f"{name} model saved to: {save_path}")


if __name__ == "__main__":
    train_and_save_models()
