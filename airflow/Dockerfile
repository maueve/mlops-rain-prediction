FROM apache/airflow:2.10.2
# Instalar herramientas de desarrollo necesarias para compilar paquetes
USER root
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    python3-dev \
    libffi-dev \
    libssl-dev \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Cambiar nuevamente al usuario por defecto de Airflow
USER airflow
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt