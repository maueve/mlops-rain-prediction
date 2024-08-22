#!/bin/bash

# Copiar el archivo model.pkl
cp ../../data/models/model.pkl .

# Construir la imagen Docker usando el Dockerfile
docker build -t servicio-inferencia-image .

# Eliminar el archivo model.pkl
rm model.pkl

# Mensaje de confirmación
echo "Proceso completado: model.pkl movido, Docker imagen construida y model.pkl eliminado."