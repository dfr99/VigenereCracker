# VigenereCracker
Repositorio para la práctica de cifrado de CSAI 23/24

## Requisitos previos

Para poder ejecutar el programa se necesita instalar [Docker](https://www.docker.com/). Opcionalmente, se requiere de  [Git](https://git-scm.com/) para clonar el repositorio.

## Instrucciones

A continuación, se muestran los comandos para construir la imagen de Docker y ejecutar el programa:

```bash
git clone https://github.com/dfr99/VigenereCracker.git
cd VigenereCracker
docker build -t estrellas_fugaces -f dist/Dockerfile .
docker run -it --rm --name estrellas_fugaces -v <ruta_fichero_cifrado_local>:<ruta_fichero_cifrado_contenedor> estrellas_fugaces <ruta_fichero_cifrado_contenedor>
```

En el caso de la entrega, como se envían los ficheros que se copian, se podrían ejecutar estos comandos:

```bash
cd codigo
docker build -t estrellas_fugaces -f dist/Dockerfile .
cd ..
docker run -it --rm --name estrellas_fugaces -v ./JdP/<nombre_fichero_cifrado>:<ruta_fichero_cifrado_contenedor> estrellas_fugaces <ruta_fichero_cifrado_contenedor>
```
