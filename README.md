# StudentPerformancePredictor
Project to learn regression and "how-build" of projects

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project.
├── datasets           <- Where the data for the project is
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. 
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         predictor and configuration for tools like black
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── predictor   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes predictor a Python module
    │
    ├── app.py                  <- Runner App
    │
    ├── model_train.py              <- Scripts to train 3 models

--------

Want to run it locall?
- Pull Repo
- Intall Requirements
    pip install -r requirements.txt

- Navigate to "predictor" directory
    fastapi dev app.py

Want to the Docker container?
- Run these commands with succession
    docker build -t predictor-app .

    docker run -it --env-file .env -p 8000:8000 predictor-app