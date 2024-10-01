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
En este ejemplo testeamos los endpoints en sí.
```sh
PYTHONPATH=$(pwd) python3 tests/test_player_methods.py 
```
Todos los archivos dentro de la carpeta `back/tests` corresponden a tests.
Recordar que el servidor debe estar funcionando para poder realizarlos. 