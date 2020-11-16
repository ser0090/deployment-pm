# Despliegue de sistemas predictivos - Práctico 1
> Diplodatos 2020

En este proyecto, construiremos y desplegaremos nuestra propia API que brindará servicios de Machine Learning, en este caso, predicción de sentimientos para oraciones en Español.

La estructura base del proyecto será la siguiente:

```
├───apps
│   └───brounder
│       │   .dockerignore
│       │   .gitignore
│       │   docker-compose.yml
│       │   Dockerfile
│       │   manage.py
│       │   README.md
│       │   requirements.txt
│       │   __init__.py
│       │
│       ├───brounder
│       │       settings.py
│       │       urls.py
│       │       wsgi.py
│       │       __init__.py
│       │
│       └───guestbook
│           │   admin.py
│           │   apps.py
│           │   models.py
│           │   tests.py
│           │   urls.py
│           │   views.py
│           │   __init__.py
│           │
│           ├───migrations
│           │       0001_initial.py
│           │       0001_initial.pyc
│           │       __init__.py
│           │       __init__.pyc
│           │
│           ├───static
│           │   └───js
│           │           controllers.js
│           │
│           └───templates
│                   index.html
│
└───kubernetes
    ├───brounder
    │       brounder.yml
    │
    ├───postgres
    │       postgres.yml
    │
    └───redis
            redis.yml
```

Su tarea será completar con el código correspondiente cada .yml de la carpeta
kubernetes y el docker-compose.yml de la carpeta apps


## Docker Swarm
---
### steps

1. iniciar docker swarm
```sh
docker swarm init
```
2. crear un stack nuevo llamdo `mystack` de docker swarm, con las instrucciones
   del `docker-compose.yml`

```sh
docker stack deploy mystack --compose-file ./docker-compose.yml
```
la capacidad de que tienen docker swarm es que trata a cada uno de los serivicos
declarados en el archivo de docker, como verdaderos servicios que pueden ser escalados
y que funcionan como un stack completo.

Ademas de cada uno de los serivicios pueden estar distribuidos.

ver los servicios

```sh
docker service ls
```

3. Replicas de Swarm
En este caso vamos a replicar un serivicio.

```sh
docker service scale mystack_web=3
```

visualizar logs para ver las respuestas de los contenedores
```sh
docker service logs mystack_web -f
```
> Note: docker swarm expone los puertos en 0.0.0.0, no en localhost.

remover stack

```sh
docker stack rm mystack
```

## traefiks
---

para escalar a 4 replicas usando docker compose
```sh
docker-compose scale whoami=4
```

la fierecian con docker swarm es que escala por stack es decir hace multiples
replicas de un sitema interconectado

Por otro lado trafiks te permite escalar sin modificar el archivos de
configuracion
