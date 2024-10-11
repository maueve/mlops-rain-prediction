import numpy as np
import pickle
import os
import mlflow

from mlflow.tracking import MlflowClient
from fastapi import FastAPI, Body, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from middleware import LogstashMiddleware

app = FastAPI()

app.add_middleware(LogstashMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




#mlflow.set_tracking_uri("http://localhost:5555")
mlflow.set_tracking_uri("http://mlflow:5000")
client = MlflowClient()
model_name = "rain-prediction"
MODEL = None

def fill_model_cache():
    """
    Funcion para cargar el modelo en cache
    :return:
    """
    global MODEL

    """
    MODEL_PATH = 'model.pkl'
    print("Model Path: ", MODEL_PATH)
    MODEL = pickle.load(open(MODEL_PATH, 'rb'))
    """

    model_version = client.get_model_version_by_alias(
        model_name, "actual"
    )

    run_id = model_version.run_id

    print("El run id es: ",run_id)

    MODEL = mlflow.sklearn.load_model(
        f"runs:/{run_id}/dtc_model",
        dst_path='./',
    )



@app.get("/predict")
def predict_rain_tomorrow(humidity: float):

    VAL_LLOVERA = 1

    llovera = False
    mensaje = ''

    data = np.array([humidity])
    data = data.reshape(-1, 1)
    res = MODEL.predict(data)

    directorio_actual = os.getcwd()

    print("El directorio actual es:", directorio_actual)

    if (res[0] == VAL_LLOVERA):
        llovera = True
        mensaje = 'Mañana llovera con una probabilidad de 83%'
    else:
        llovera = False
        mensaje = 'Mañana NO llovera con una probabilidad de 83%'

    return  {
        'llovera': llovera,
        'mensaje': mensaje
    }


@app.get("/refresh_model/")
async def refresh_models():
    """
    Funcion para refrescar modelos mediante api
    :return:
    """
    fill_model_cache()
    return {"status": "success"}

fill_model_cache()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





