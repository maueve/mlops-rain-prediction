import os
import time
import mlflow
import pickle
import logging

import pandas as pd

from pathlib import Path
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from ydata_profiling import ProfileReport
from mlflow.exceptions import RestException
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient


from plots import (
    create_confusion_matrices,
    create_learning_curves,
    plot_feature_importance,
)
from reports import make_classification_report_frame






def training_and_publish():
    # Obtener el directorio actual
    directorio_actual = os.getcwd()
    print("El directorio actual es:", directorio_actual)

    logging.info(f"el directorio actual es {directorio_actual}")

    #Creacion del directorio de artefactos
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    #print(output_dir.resolve())

    logging.info("Iniciando proceso")

    mlflow.set_tracking_uri("http://mlflow:5000")
    #mlflow.set_tracking_uri("http://localhost:5000")

    mlflow.set_experiment("Test Rain Prediction")
    mlflow.set_experiment_tags(
        {
            "project": "Rain Prediction",
            "task": "Prediction",
        }
    )
    run = mlflow.start_run()

    logging.info("Antes de leer el achivo")


    FILE = directorio_actual +'/dags/weather_data.csv'
    df = pd.read_csv(FILE)

    logging.info(f"Tamnao del dataset: {df.shape} " )

    # Para genear un reporte de datos
    data_report = ProfileReport(df, title="Data Report")
    data_report.to_file(output_dir / "data_report.html")
    mlflow.log_artifact(output_dir / "data_report.html")


    X = df.loc[:,df.columns!='RainTomorrow']
    y = df[['RainTomorrow']]

    num_features = 3
    mlflow.log_param("num_features", num_features)

    selector = SelectKBest(chi2, k=num_features)
    selector.fit(X, y)
    X_new = selector.transform(X)
    print(X.columns[selector.get_support(indices=True)]) #top 3 columnas


    df = df[['Humidity3pm','Rainfall','RainToday','RainTomorrow']]
    X = df[['Humidity3pm']] #Solo se usara la caracteristica Humidity3pm
    y = df[['RainTomorrow']]


    test_size=0.25
    random_state=0

    mlflow.log_param("test_size", test_size)
    mlflow.log_param("random_state", random_state)


    #Entrenamiento del modelo
    t0=time.time()
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=test_size)

    mlflow.log_param("x_train_shape", X_train.shape)
    mlflow.log_param("x_test_shape", X_test.shape)
    mlflow.log_param("y_train_shape", y_train.shape)
    mlflow.log_param("y_test_shape", y_test.shape)

    model = DecisionTreeClassifier(random_state=random_state)
    model.fit(X_train.values,y_train)

    execution_time = time.time() - t0
    print('Tiempo de Ejecucion :', execution_time)
    mlflow.log_metric("execution_time", execution_time)

    mlflow.log_params({
        f"dtc_{param}": value for param, value in model.get_params().items()
    })

    MODEL_FILE = output_dir / "model.pkl"

    with open(MODEL_FILE, 'wb') as archivo:
        pickle.dump(model, archivo)

    mlflow.log_artifact(str(MODEL_FILE))

    #Obtener la firma del modelo
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(model, "dtc_model", signature=signature)

    #Registro del modelo
    model_name = "rain-prediction"
    model_version = mlflow.register_model(
        model_uri=f"runs:/{run.info.run_id}/dtc_model",
        name=model_name
    )


    #Registro de Alias
    client = MlflowClient()
    model_alias = "actual"

    client.set_registered_model_alias(model_version.name, model_alias, model_version.version)

    ######################
    #Evaluacion del modelo
    ######################
    y_pred = model.predict(X_test.values)
    test_accuracy = accuracy_score(y_test,y_pred)

    print('Accuracy :',test_accuracy)
    mlflow.log_metric("test_accuracy", test_accuracy)

    # Create a learning curve plot
    learning_curve_figure = create_learning_curves(model, X_train, y_train)
    mlflow.log_figure(learning_curve_figure, "learning_curve.png")

    print(f"Model version: {model_version.name} {model_version.version}")
    print(f"Experiment ID: {run.info.experiment_id}")
    print(f"Run ID: {run.info.run_id}")