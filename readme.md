# Proyecto de Prediccion de LLuvia y MLOps

El presente proyecto integra el desarrollo de un proyecto de machine learning para 
la prediccion de lluvia, con practicas de MLOps para el despliegue y monitoreo de modelos

### Dataset
El dataset es un conjunto de datos de observaciones usado para predecir si llovera o no en varias
localidades de Australia

[Dataset](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package)

## Requisitos

Para correr este proyecto, es necesario tener Docker instalado. Además, se requiere crear las imágenes Docker necesarias para los servicios y la interfaz web.

## Pasos para Ejecutar el Proyecto

### 1. Crear la red extrerna para cointainers

```bash
docker network create shared_network
```

### 2. Registrar el modelo

En la carpeta raíz del proyecto para levantar MLFLow usar el siguiente comando:

```bash
docker compose -f docker-compose_training.yml --env-file training.env up
```

Desde la carpeta raíz moverse al directorio notebooks:

```bash
cd notebooks
```

Y  ejecutar el siguiente scrip de python:

```bash
python test_training.py 
```


### 3. Ejecutar el Proyecto

Para iniciar el proyecto, primero de debe de incializar el monitoreo, en la carpeta docker-elk, desde la carpeta raiz ejecutar:

```bash
cd  docker-elk
```

```bash
docker compose up setup  
```

Después ejecutar:

```bash
docker compose up 
```

Ahora en la carpeta raíz del proyecto, correr el siguiente comando:
```bash
docker compose up 
```



### 4. Acceder a la Aplicacion

Para ingresar a la página principal de la aplicación:

http://localhost:8080/

Para acceder directamente a la API ingresar con la siguiente url:

http://127.0.0.1:8000/predict?humidity=0.8

Para acceder a la definicion de la API ingresar con la siguiente url:

http://localhost:8000/docs


### 5. Acceder a la Infraestructura

Para ingresar a Kibana:

http://localhost:5601/

Para ingesar a MLFlow

http://localhost:5555/


