## Instrucciones para correr el codigo

1. Crear una base de datos en MySQL.
```sql
CREATE DATABASE proyecto;
```

2. Usar la base de datos recien creada.
```sql
USE proyecto;
```

3. Ejecutar el contenido del archivo [schema.sql](https://github.com/gmr458/proyecto/blob/main/schema.sql) para crear las tablas.

4. Crear en la raiz del proyecto un archivo `.env` y alli poner los valores de configuración para la conexión con la base de datos.

```sh
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DBNAME=dbname
```

5. Crear un entorno virtual de Python con el siguiente comando:
```sh
python3 -m venv venv
```

6. Activar el entorno virtual con el siguiente comando:

En Linux:
```sh
source venv/bin/activate
```

7. Instalar las dependencias con el siguiente comando:
```sh
pip install -r requirements.txt
```

8. Ejecutar el siguiende comando en la raiz del proyecto.
```sh
uvicorn app.main:app --reload
```
