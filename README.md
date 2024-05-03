# VigenereCracker
Repositorio para la práctica de cifrado de CSAI 23/24

## Requisitos previos

Para poder ejecutar el programa se necesita instalar [Docker](https://www.docker.com/)

## Instrucciones

A continuación, se muestran los comandos para construir la imagen de Docker y ejecutar el programa:

```bash
git clone https://github.com/dfr99/VigenereCracker.git
cd VigenereCracker 
docker build -t estrellas_fugaces -f dist/Dockerfile .
docker exec -it --rm --name estrellas_fugaces estrellas_fugaces <fichero_alfabeto> <fichero_texto_cifrado>
```
