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

### 1. Crear Imágen Docker para los Servicios

En la carpeta `src/services/`, ejecuta el siguiente script para crear las imágenes Docker necesarias:

```bash
sh crear_imagen.sh
```

### 2. Crear la Imagen Docker para la Interfaz Web

En la carpeta src/web/, ejecuta el siguiente comando para construir la imagen Docker de la interfaz web:

```bash
docker build -t web-clima-image .
```

### 3. Ejecutar el Proyecto

Para iniciar el proyecto ejecuta:

```bash
python src/main.py
```

### 4. Acceder a la Aplicacion

Para acceder a la definicion de la API ingresar con la siguiente url:

http://localhost:8000/docs

Para ingresar a la página principal de la aplicación:

http://localhost:8080/


