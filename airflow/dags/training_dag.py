from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from training import (
    training_and_publish
)

# Función que ejecutará la tarea Python
def my_task2():
    print("Hello from Airflow Task!")


# Función que ejecutará la tarea Python
def my_task():
    training_and_publish()

# Definir los argumentos del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 7),  # Fecha en que el DAG comenzará a correr
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Crear el DAG
dag = DAG(
    'training_dag',                 # Identificador único del DAG
    default_args=default_args,       # Argumentos por defecto
    description='Dag de entrenamiento de modelo de predccion de lluvia',      # Descripción del DAG
    schedule_interval=None,  # Frecuencia: cada día
)

# Definir la tarea
task1 = PythonOperator(
    task_id='training',
    python_callable=my_task,  # Función a ejecutar
    dag=dag,                  # Asociar la tarea con el DAG
)

# Para este ejemplo, solo tenemos una tarea, así que no es necesario definir dependencias.
