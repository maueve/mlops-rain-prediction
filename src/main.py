import docker

# Crear una instancia del cliente Docker
client = docker.from_env()

# Definir las configuraciones para los contenedores
container1_config = {
    'image': 'servicio-inferencia-image',
    'command': 'uvicorn prediction_service:app --host 0.0.0.0 --port 8000',
    'detach': True,
    'ports': {'8000/tcp': 8000},
    'name': 'servicio-inferencia-app'
}

container2_config = {
    'image': 'web-clima-image',
    'command': 'flask run --host=0.0.0.0 --port=8080',
    'detach': True,
    'ports': {'8080/tcp': 8080},
    'name': 'web-clima-app'
}

# Lanzar el primer contenedor
container1 = client.containers.run(**container1_config)
print(f"Contenedor 1 lanzado: {container1.id}")

# Lanzar el segundo contenedor
container2 = client.containers.run(**container2_config)
print(f"Contenedor 2 lanzado: {container2.id}")

# Opcional: Esperar a que los contenedores terminen
container1.wait()
container2.wait()

print(f"Contenedor 1 completado con estado: {container1.status}")
print(f"Contenedor 2 completado con estado: {container2.status}")
