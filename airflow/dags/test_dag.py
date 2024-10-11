from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Función que ejecutará la tarea Python
def my_task():
    print("Hello from Airflow Task!")

# Definir los argumentos del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 7),  # Fecha en que el DAG comenzará a correr
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Crear el DAG
dag = DAG(
    'my_first_dag',                 # Identificador único del DAG
    default_args=default_args,       # Argumentos por defecto
    description='My First DAG',      # Descripción del DAG
    schedule_interval=timedelta(days=1),  # Frecuencia: cada día
)

# Definir la tarea
task1 = PythonOperator(
    task_id='print_hello',
    python_callable=my_task,  # Función a ejecutar
    dag=dag,                  # Asociar la tarea con el DAG
)

# Para este ejemplo, solo tenemos una tarea, así que no es necesario definir dependencias.
