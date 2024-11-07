
# Switcher - backend


## LINUX  

### Cómo correr

Para levantar el servidor, ejecutar la siguiente serie de comandos:

```sh

git  clone  https://github.com/LavajabonSinRopa/back.git

cd  back

  

# Crear y activar un virtual environment, e instalar las dependencias

python3  -m  venv  .venv

source  .venv/bin/activate

pip  install  -r  requirements.txt

  

# Levantar el servidor

python3  src/main.py

```

  

### Cómo testear

Los diferentes tests se encuentran modularizados en distintos archivos según la funcionalidad.

  

**Para correr todos los tests**:

```sh

coverage  run  tests/run.py  -v  tests

```

  

----

  

Para correr todos los tests y ver reporte de coverage en la terminal:

```sh

coverage  run  tests/run.py  -v  tests && coverage  report  -m

```

  

Para correr todos los tests y ver reporte de coverage en pagina web:

```sh

coverage  run  tests/run.py  -v  tests && coverage  html && open  htmlcov/index.html

```

  

----

  

## WINDOWS


### Cómo correr

Para levantar el servidor, ejecutar la siguiente serie de comandos:

```sh

git  clone  https://github.com/LavajabonSinRopa/back.git

cd  back

  

# Crear y activar un virtual environment, e instalar las dependencias

py  -m  venv  .venv

.venv\Scripts\activate.bat

pip  install  -r  requirements.txt

  

# Levantar el servidor

py  src/main.py

```

  

### Cómo testear

Los diferentes tests se encuentran modularizados en distintos archivos según la funcionalidad.

  

**Para correr todos los tests**:

```sh

coverage  run  tests/run.py  -v  tests

```

  

----

  

Para correr todos los tests y ver reporte de coverage en la terminal:

```sh

coverage  run  tests/run.py  -v  tests && coverage  report  -m

```

  

Para correr todos los tests y ver reporte de coverage en pagina web:

```sh

coverage  run  tests/run.py  -v  tests && coverage  html && start  htmlcov/index.html

```

---

## LavajabonSinRopa

Este proyecto fue desarrollado por:

 ### Back
 - José Mochkofsky
 - Ivo Pfaffen
 - Francisco Sabaté

### Front

 - Luca Reynaldo
 - Martina Ibañez
 - Franco Avalos
