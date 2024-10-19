## Switcher - backend

### Cómo correr
Para levantar el servidor, ejecutar la siguiente serie de comandos:
```sh
git clone https://github.com/LavajabonSinRopa/back.git
cd back

# Crear y activar un virtual environment, e instalar las dependencias
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Levantar el servidor
python3 src/main.py
```

### Cómo testear
Los diferentes tests se encuentran modularizados en distintos archivos según la funcionalidad.

Para correr todos los tests y ver reporte de coverage en la terminal:
```sh
coverage run tests/run.py -v tests && coverage report -m
```

Para correr todos los tests y ver reporte de coverage en pagina web:
```sh
coverage run tests/run.py -v tests && coverage html && open htmlcov/index.html
```

Para testear todo excepto WebSockets (no es necesario tener el back levantado):
```sh
coverage run tests/run.py -v tests -k "not test_websocket_game and not test_websocket_public" && coverage html && open htmlcov/index.html
```

Ahora bien, para testear sólo los relacionados a WebSockets (es necesario tener el back levantado):
```sh
coverage run tests/run.py -v tests -k "test_websocket_game or test_websocket_public" && coverage html && open htmlcov/index.html
```

Todos los archivos dentro de la carpeta `back/tests` corresponden a tests.
Recordar que el servidor debe estar funcionando para poder realizarlos. 